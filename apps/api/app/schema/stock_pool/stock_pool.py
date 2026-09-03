from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator


def local_now() -> datetime:
    return datetime.now()


class StockPoolCreate(BaseModel):
    project_id: str = Field(min_length=1, max_length=128)
    name: str = Field(min_length=1, max_length=128)
    description: str | None = None

    model_config = ConfigDict(extra="forbid")


class StockPoolUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=128)
    description: str | None = None

    model_config = ConfigDict(extra="forbid")


class StockPoolRecord(BaseModel):
    id: str
    project_id: str
    name: str
    description: str | None = None
    stock_count: int = 0
    created_at: datetime = Field(default_factory=local_now)
    updated_at: datetime = Field(default_factory=local_now)


class StockPoolListResponse(BaseModel):
    items: list[StockPoolRecord] = Field(default_factory=list)
    total: int = 0


class StockPoolStockCreate(BaseModel):
    symbol: str = Field(min_length=1, max_length=64)
    name: str | None = Field(default=None, max_length=128)
    tags: list[str] = Field(default_factory=list)
    note: str | None = None

    model_config = ConfigDict(extra="forbid")

    @model_validator(mode="after")
    def normalize(self) -> StockPoolStockCreate:
        self.symbol = normalize_symbol(self.symbol)
        self.name = _blank_to_none(self.name)
        self.note = _blank_to_none(self.note)
        self.tags = normalize_tags(self.tags)
        return self


class StockPoolStocksBulkCreate(BaseModel):
    symbols: str = Field(min_length=1)

    model_config = ConfigDict(extra="forbid")


class StockPoolStockUpdate(BaseModel):
    symbol: str | None = Field(default=None, min_length=1, max_length=64)
    name: str | None = Field(default=None, max_length=128)
    tags: list[str] | None = None
    note: str | None = None

    model_config = ConfigDict(extra="forbid")

    @model_validator(mode="after")
    def normalize(self) -> StockPoolStockUpdate:
        if self.symbol is not None:
            self.symbol = normalize_symbol(self.symbol)
        if self.name is not None:
            self.name = _blank_to_none(self.name)
        if self.note is not None:
            self.note = _blank_to_none(self.note)
        if self.tags is not None:
            self.tags = normalize_tags(self.tags)
        return self


class StockPoolStockRecord(BaseModel):
    id: str
    pool_id: str
    symbol: str
    name: str | None = None
    tags: list[str] = Field(default_factory=list)
    note: str | None = None
    created_at: datetime = Field(default_factory=local_now)
    updated_at: datetime = Field(default_factory=local_now)


class StockPoolDetail(StockPoolRecord):
    stocks: list[StockPoolStockRecord] = Field(default_factory=list)
    symbols: list[str] = Field(default_factory=list)


class StockPoolStockListResponse(BaseModel):
    items: list[StockPoolStockRecord] = Field(default_factory=list)
    total: int = 0


class StockPoolBulkCreateResult(BaseModel):
    items: list[StockPoolStockRecord] = Field(default_factory=list)
    created: int = 0
    skipped: int = 0


class StockPoolCandidate(BaseModel):
    symbol: str
    name: str | None = None
    in_pool: bool = False


class StockPoolCandidateListResponse(BaseModel):
    items: list[StockPoolCandidate] = Field(default_factory=list)
    total: int = 0


class StockPoolSnapshotImportResult(BaseModel):
    items: list[StockPoolStockRecord] = Field(default_factory=list)
    created: int = 0
    skipped: int = 0
    source_dataset: str = "a_stock_snapshot_info"


class StockPoolSnapshotImportRequest(BaseModel):
    symbols: list[str] = Field(default_factory=list)

    model_config = ConfigDict(extra="forbid")

    @model_validator(mode="after")
    def normalize(self) -> StockPoolSnapshotImportRequest:
        symbols: list[str] = []
        for symbol in self.symbols:
            normalized = normalize_symbol(symbol)
            if normalized and normalized not in symbols:
                symbols.append(normalized)
        self.symbols = symbols
        return self


def normalize_symbol(symbol: str) -> str:
    return symbol.strip().upper()


def split_symbols(value: str) -> list[str]:
    normalized = (
        value.replace("，", ",")
        .replace("；", ",")
        .replace(";", ",")
        .replace("\n", ",")
        .replace("\t", ",")
        .replace(" ", ",")
    )
    symbols: list[str] = []
    for part in normalized.split(","):
        symbol = normalize_symbol(part)
        if symbol and symbol not in symbols:
            symbols.append(symbol)
    return symbols


def normalize_tags(tags: list[str]) -> list[str]:
    normalized: list[str] = []
    for tag in tags:
        stripped = str(tag).strip()
        if stripped and stripped not in normalized:
            normalized.append(stripped[:32])
    return normalized


def _blank_to_none(value: str | None) -> str | None:
    if value is None:
        return None
    stripped = value.strip()
    return stripped or None
