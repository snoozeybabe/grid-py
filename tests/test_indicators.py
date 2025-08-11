import pandas as pd
import numpy as np
from src.indicators_lib import add_indicators

def main():
    n = 120
    idx = pd.date_range("2025-08-10", periods=n, freq="T", tz="UTC")
    base = 100 + np.cumsum(np.random.randn(n)) * 0.1
    df = pd.DataFrame({
        "open": base + np.random.randn(n) * 0.1,
        "high": base + np.abs(np.random.randn(n)) * 0.05,
        "low": base - np.abs(np.random.randn(n)) * 0.05,
        "close": base + np.random.randn(n) * 0.01,
        "volume": np.random.randint(50,500,size=n),
    }, index=idx)
    out = add_indicators(df, ema_len=20, atr_len=14)
    assert "EMA" in out.columns and "ATR" in out.columns
    assert out["EMA"].notna().all() and out["ATR"].notna().all()
    print("test_indicators : OK - EMA and ATR computed via pandas-TA.")
    print(out[:10])
if __name__ == "__main__":
    main()