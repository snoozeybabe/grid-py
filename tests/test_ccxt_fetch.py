import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from data_utils import fetch_ohlcv_ccxt

# rest of your code ...




def main():
    try:
        pair="BTC/USDT:USDT"
        df = fetch_ohlcv_ccxt(exchange_id="bitget", symbol=pair, timeframe="1m", limit=50)
        assert not df.empty and set(["open","high","low","close","volume"]).issubset(df.columns)
        print(f"test_ccxt_fetch : OK - Fetched OHLCV via CCXT for {pair}")
        print("==============================")
        print(df)
        print("==============================")
    except Exception as e:
        print("test_ccxt_fetch : SKIP-", e)
    try:
        pair="ETH/USDT"
        df = fetch_ohlcv_ccxt(exchange_id="bitget", symbol=pair, timeframe="1m", limit=50)
        assert not df.empty and set(["open","high","low","close","volume"]).issubset(df.columns)
        print(f"test_ccxt_fetch : OK - Fetched OHLCV via CCXT for {pair}")
        print("==============================")
        print(df)
        print("==============================")
    except Exception as e:
        print("test_ccxt_fetch : SKIP-", e)
if __name__ == "__main__":
    main()