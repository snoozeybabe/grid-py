import pandas as pd
from typing import Optional
import time

def preprocess(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()
    df = df.rename(columns={c: c.lower() for c in df.columns})
    required = ["open", "high", "low", "close", "volume"]
    for r in required:
        if r not in df.columns:
            raise ValueError(f"Missing column: {r}")
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
        df = df.set_index("timestamp")
    df = df.sort_index()
    df = df[required]
    return df

def load_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    # Try to detect timestamp column
    ts_col = None
    for c in ["timestamp", "time", "date", "Datetime", "datetime"]:
        if c in df.columns:
            ts_col = c
            break
    if ts_col is None:
        raise ValueError("No timestamp column found in CSV.")
    df["timestamp"] = pd.to_datetime(df[ts_col], utc=True)
    df = df.drop(columns=[ts_col], errors="ignore")
    df = df.rename(columns={c: c.lower() for c in df.columns})
    df = df.set_index("timestamp").sort_index()
    df = df[["open","high","low","close","volume"]]
    return df

def fetch_ohlcv_ccxt(exchange_id: str = "bitget", symbol: str = "BTC/USDT:USDT", timeframe: str = "1m", limit: int = 1000):
    """
    Fetch OHLCV via ccxt and return a preprocessed DataFrame with UTC index and OHLCV columns.
    Note: Requires network access; exchanges may rate-limit.
    """
    import ccxt
    ex = getattr(ccxt, exchange_id)({"enableRateLimit": True})
    # Some exchanges require load_markets() for precision rules; not strictly needed for fetch_ohlcv.
    ohlcv = ex.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=["timestamp","open","high","low","close","volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True)
    df = df.set_index("timestamp").sort_index()
    return preprocess(df)