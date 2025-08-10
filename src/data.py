import os
import pandas as pd
from typing import Optional


try:
    import yfinance as yf
except Exception:
    print("Please install the required packages.")
    yf = None


def load_csv(path: str, tz: Optional[str] = None) -> pd.DataFrame:
    df  = pd.read_csv(path)
    ts_col = None
    for c in ["timestamp", "time", "date","Datetime", "datetime"]:
        if c in df.columns:
            ts_col = c
            break
    if ts_col is None:
        raise ValueError("No timestamp column found in CSV.")
    
    df[ts_col] = pd.to_datetime(df[ts_col], utc=True)
    if tz:
        df[ts_col] = pd.to_datetime(df[ts_col]).dt.tz_localize(tz).dt.tz_convert("UTC")
    
    df = df.set_index(ts_col).sort_index()
    rename_map = {c :c.lower() for c in df.columns}
    df = df.rename(columns=rename_map)
    required = ["open", "high", "low", "close", "volume"]
    for r in required:
        if r not in df.columns:
            raise ValueError(f"Required column {r} not found in CSV.")
    return df[required]

def download_yfinance_1m(symbol : str, start : str, end : Optional[str]= None) -> pd.DataFrame:
    if yf is None:
        raise ImportError("Yahoo Finance not installed. Please install it using pip install yfinance or use CSV.")
    df = yf.download(symbol, interval="1m", start=start, end=end, progress=False)
    if df.empty:
        raise ImportError("No data found for the given symbol and time range")
    df = df.tz_convert("UTC")
    df = df.rename(columns=str.lower)
    df = df[["open", "high", "low", "close", "volume"]]
    return df

def preprocess(df : pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = df[~df.index.duplicated(keep="first")].sort_index()
    df = df.dropna()
    for c in ["open", "high", "low", "close"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna()
    return df
    
    

