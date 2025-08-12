import pandas as pd
import numpy as np
from src.live_ccxt import compute_grid

def main():
    n = 100
    idx = pd.date_range(start="2025-08-01", periods=n, freq="1min", tz="UTC")
    base = 20000 + np.cumsum(np.random.randn(n))*5
    df = pd.DataFrame({
        "open" : base + np.random.randn(n),
        "high" : base + np.abs(np.random.randn(n))*3,
        "low" : base - np.abs(np.random.randn(n))*3,
        "close" : base + np.random.randn(n),
        "volume" : np.random.randint(10,1000,size=n)
    },index=idx)
    ema,atr,step,buys,sells = compute_grid(df)
    assert len(buys) > 0 and len(sells) > 0
    assert step > 0
    print(f"test_live_grid: OK - EMA={ema:.2f} ATR={atr:.2f} Step={step:.2f} levels={len(buys) + len(sells)}")


if __name__ == "__main__":
    main()