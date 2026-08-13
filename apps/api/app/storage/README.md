# DuckDB Parquet Storage

This package defines the local analytical storage boundary.

## Responsibilities

`DuckDBParquetStore` is a general-purpose adapter for reading and writing Parquet through DuckDB.

It owns:

- DataFrame to Parquet writes.
- SQL queries over Parquet files.
- Atomic file replacement during writes.

It does not own:

- MindGo dataset semantics.
- Sync scheduling or import workflows.
- SQLite metadata tables.
- Persistent DuckDB database files.
- Business-level schema validation.

## Engine Rule

All Parquet reads must go through DuckDB.

Business code should not call:

- `pandas.read_parquet`
- `pandas.DataFrame.to_parquet`
- `pyarrow.dataset`
- direct `duckdb` APIs

The storage module is the only layer that should import DuckDB.

## Runtime Model

DuckDB is used as an execution engine only:

```python
duckdb.connect(":memory:")
```

The module must not create or depend on a persistent `.duckdb` database file.

## Suggested Data Layout

MindGo can use this generic layout from its own service layer:

```text
data/
  mindgo/
    parquet/
      stock_a_daily_price/
        trade_year=2024/
          data.parquet
        trade_year=2025/
          data.parquet
        trade_year=2026/
          data.parquet
```

The storage module does not create this structure by itself. Callers choose paths and partition keys.

## Public Interface

```python
store = DuckDBParquetStore()
```

Read data by writing DuckDB SQL:

```python
frame = store.query(
    """
    SELECT symbol, close
    FROM read_parquet($path)
    WHERE trade_date = $trade_date
    """,
    params={
        "path": "data/mindgo/parquet/stock_a_daily_price/trade_year=*/data.parquet",
        "trade_date": "2026-08-13",
    },
)
```

Write one Parquet file:

```python
count = store.write(
    frame,
    "data/mindgo/parquet/stock_a_daily_price/trade_year=2026/data.parquet",
    options=ParquetWriteOptions(order_by=["trade_date", "symbol"]),
)
```

## Method Contracts

`query()`:

- Registers optional DataFrames as temporary DuckDB relations.
- Executes caller-provided SQL.
- Returns a pandas DataFrame.

`write()`:

- Registers the DataFrame with DuckDB.
- Writes with `COPY ... TO ... (FORMAT PARQUET)`.
- Uses compression, defaulting to `zstd`.
- Replaces the target atomically after a successful write.
- Returns written row count.
