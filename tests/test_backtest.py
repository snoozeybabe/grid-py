import pandas as pd
import numpy as np
from backtesting import Backtest
from src.indicators_lib import add_indicators
from src.grid_strategy import GridScalperBT


def make_synth_1m(n=600):
    idx = pd.date_range("2025-08-01", periods=n, freq="T", tz="UTC")
    trend = np.sin(np.linspace(0, 8*np.pi,n)) * 0.5
    noise = np.cumsum(np.random.randn(n))*0.03
    close = 100 + trend + noise
    open_ = close + np.random.randn(n) * 0.01
    high = close + np.abs(np.random.randn(n)) * 0.05
    low = close - np.abs(np.random.randn(n)) * 0.05
    vol = np.random.randint(50,1000,size=n)
    df = pd.DataFrame({"open": open_, "high": high, "low": low, "close": close, "volume": vol}, index=idx)
    return df

def main():
    df = make_synth_1m(15000)
    df = add_indicators(df, ema_len=50,atr_len=14)
    df_bt = df.rename(columns={"open":"Open","high":"High","low":"Low","close":"Close","volume":"Volume"})
    bt = Backtest(
        df_bt,
        GridScalperBT,
        cash=10000, 
        commission=0.0002,
        exclusive_orders=False
    )
    stats =bt.run(
        level_each_side=4,
        step_k=0.6,
        min_step=0.0,
        recenter_k=1.5,
        atr_hysteresis=0.25,
        stop_steps=3.0,
        allow_shorts=False,
        size=0.01
    )
    bt.plot()
    assert "Equity Final [$]" in stats, "Backtest failed to run"
    print("test_backtest: OK - backtest ran with dynamic grid")
    print(stats[["# Trades", "Win Rate [%]", "Return [%]", "Max. Drawdown [%]" ]])

if __name__ == "__main__":
    main()
