---
source_url: local extracted Python pattern from portable Jupyter case
ingested: 2026-08-11
sha256: 3f95a63b9fc640bfda2fe7fe692278319d44e2d2466c956210cfbe0699e684e6
---

# Jupyter Python pattern: A-share 1-minute bars with get_price

```python
import json
import math
import traceback
import pandas as pd

TRADE_DATE = "20260710"
STOCK_LIST = ["000001.SZ", "600000.SH"]
START_TIME = TRADE_DATE + " 09:30"
END_TIME = TRADE_DATE + " 10:30"
FIELDS = ["close", "high", "low", "open", "volume", "turnover"]
MARKER_START = "MINDGO_INTRADAY_JSON_START"
MARKER_END = "MINDGO_INTRADAY_JSON_END"


def json_value(value):
    if value is None:
        return None
    try:
        if pd.isna(value):
            return None
    except Exception:
        pass
    try:
        if hasattr(value, "item"):
            value = value.item()
    except Exception:
        pass
    if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
        return None
    if isinstance(value, (str, int, float, bool)):
        return value
    return str(value)


def frame(value, field):
    if isinstance(value, dict):
        data = value.get(field)
    else:
        try:
            data = value[field]
        except Exception:
            data = getattr(value, field, None)
    return None if data is None else pd.DataFrame(data)


def time_text(value):
    if hasattr(value, "strftime"):
        return value.strftime("%H:%M")
    text = str(value)
    return text[-8:-3] if len(text) >= 16 and ":" in text else text[:5]


def cell(frame_obj, ts, stock):
    if frame_obj is None or frame_obj.empty:
        return None
    for candidate in (stock, stock.split(".")[0]):
        if candidate in frame_obj.columns:
            return json_value(frame_obj.loc[ts, candidate])
    if len(frame_obj.columns) == 1:
        return json_value(frame_obj.loc[ts, frame_obj.columns[0]])
    return None

payload = {"source": "mindgo_get_price", "trade_date": TRADE_DATE, "items": {}}
try:
    value = get_price(STOCK_LIST, START_TIME, END_TIME, "1m", FIELDS, True, None, 0, is_panel=1)
    frames = {field: frame(value, field) for field in FIELDS}
    all_times = sorted({idx for f in frames.values() if f is not None for idx in list(f.index)})
    for stock in STOCK_LIST:
        rows = []
        for ts in all_times:
            row = {
                "stockcode": stock,
                "trade_date": TRADE_DATE,
                "bar_time": time_text(ts),
                "open": cell(frames.get("open"), ts, stock),
                "high": cell(frames.get("high"), ts, stock),
                "low": cell(frames.get("low"), ts, stock),
                "close": cell(frames.get("close"), ts, stock),
                "volume": cell(frames.get("volume"), ts, stock),
                "amount": cell(frames.get("turnover"), ts, stock),
            }
            if any(row[k] is not None for k in ("open", "high", "low", "close")):
                rows.append(row)
        payload["items"][stock] = rows
except Exception as exc:
    payload["error"] = str(exc)
    payload["traceback"] = traceback.format_exc(limit=5)

print(MARKER_START)
print(json.dumps(payload, ensure_ascii=False, separators=(",", ":")))
print(MARKER_END)
```

The important method is not the wrapper around it; it is the remote Jupyter script: call get_price in the MindGo kernel, normalize Panel/dict/DataFrame output, print marked JSON, then parse it locally.
