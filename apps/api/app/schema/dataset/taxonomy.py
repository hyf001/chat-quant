from __future__ import annotations

from enum import StrEnum


class DatasetMarket(StrEnum):
    A = "A股"
    HK = "港股"
    US = "美股"


class DatasetAssetClass(StrEnum):
    STOCK = "股票"
    FUND = "基金"
    INDEX = "指数"
    MARKET = "市场"


class DatasetFrequency(StrEnum):
    TICK = "逐笔"
    MINUTE = "分钟"
    DAILY = "日"
    WEEKLY = "周"
    MONTHLY = "月"
    QUARTERLY = "季"
    YEARLY = "年"
    SNAPSHOT = "快照"
    STATIC = "静态"


MARKET_ENGLISH: dict[DatasetMarket, str] = {
    DatasetMarket.A: "a",
    DatasetMarket.HK: "hk",
    DatasetMarket.US: "us",
}

ASSET_CLASS_ENGLISH: dict[DatasetAssetClass, str] = {
    DatasetAssetClass.STOCK: "stock",
    DatasetAssetClass.FUND: "fund",
    DatasetAssetClass.INDEX: "index",
    DatasetAssetClass.MARKET: "market",
}

FREQUENCY_ENGLISH: dict[DatasetFrequency, str] = {
    DatasetFrequency.TICK: "tick",
    DatasetFrequency.MINUTE: "minute",
    DatasetFrequency.DAILY: "daily",
    DatasetFrequency.WEEKLY: "weekly",
    DatasetFrequency.MONTHLY: "monthly",
    DatasetFrequency.QUARTERLY: "quarterly",
    DatasetFrequency.YEARLY: "yearly",
    DatasetFrequency.SNAPSHOT: "snapshot",
    DatasetFrequency.STATIC: "static",
}


def dataset_name_zh(
    market: DatasetMarket,
    asset_class: DatasetAssetClass,
    frequency: DatasetFrequency,
    topic_zh: str,
) -> str:
    return f"{market.value}{asset_class.value}{frequency.value}{topic_zh}"


def dataset_name_en(
    market: DatasetMarket,
    asset_class: DatasetAssetClass,
    frequency: DatasetFrequency,
    topic_en: str,
) -> str:
    return "_".join(
        [
            MARKET_ENGLISH[market],
            ASSET_CLASS_ENGLISH[asset_class],
            FREQUENCY_ENGLISH[frequency],
            topic_en,
        ]
    )


def category_path(
    market: DatasetMarket,
    asset_class: DatasetAssetClass,
    frequency: DatasetFrequency,
    topic_zh: str,
) -> list[str]:
    return [market.value, asset_class.value, frequency.value, topic_zh]


def category_path_en(
    market: DatasetMarket,
    asset_class: DatasetAssetClass,
    frequency: DatasetFrequency,
    topic_en: str,
) -> list[str]:
    return [
        MARKET_ENGLISH[market],
        ASSET_CLASS_ENGLISH[asset_class],
        FREQUENCY_ENGLISH[frequency],
        topic_en,
    ]
