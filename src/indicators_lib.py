import pandas as pd
import pandas_ta as ta

def add_indicators(df: pd.DataFrame, ema_len: int = 50, atr_len: int = 14) -> pd.DataFrame:
    out = df.copy()
    out["EMA"] = ta.ema(out["close"], length=ema_len)
    out["ATR"] = ta.atr(out["high"], out["low"], out["close"], length=atr_len)
    return out.dropna()
