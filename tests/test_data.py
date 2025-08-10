import sys
import os
import numpy as np
import pandas as pd

# Add the parent directory of 'src' to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data import preprocess

def make_synth_1m(n=180):
    idx = pd.date_range("2025-08-01", periods=n, freq="min", tz="UTC")
    prices = 100 + np.cumsum(np.random.randn(n)) * 0.2
    high = prices + np.random.rand(n) * 0.1
    low = prices - np.random.rand(n) * 0.1
    open_ = prices + np.random.randn(n) * 0.02
    close = prices + np.random.randn(n) * 0.02
    vol = np.random.randint(10,1000, size=n)
    df = pd.DataFrame({
        "open" : open_,
        "high" : high,
        "low" : low,
        "close" : close,
        "volume" : vol,
    }, index=idx)
    return df

def main():
    df = make_synth_1m(200)
    df = preprocess(df)
    assert not df.empty, "Preprocessed DataFrame is empty"
    assert set(["open", "high", "low", "close", "volume"]).issubset(df.columns), "Columns are missing from the preprocessed DataFrame"
    print("All tests passed!")

if __name__ == "__main__":
    main()
