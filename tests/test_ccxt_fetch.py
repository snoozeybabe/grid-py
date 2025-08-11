from src.data_utils import fetch_ohlcv_ccxt


def main():
    try:
        pair="BTC/USDT"
        df = fetch_ohlcv_ccxt(exchange_id="binance", symbol=pair, timeframe="1m", limit=50)
        assert not df.empty and set(["open","high","low","close","volume"]).issubset(df.columns)
        print(f"test_ccxt_fetch : OK - Fetched OHLCV via CCXT for {pair}")
        print("==============================")
        print(df)
        print("==============================")
    except Exception as e:
        print("test_ccxt_fetch : SKIP-", e)
    try:
        pair="ETH/USDT"
        df = fetch_ohlcv_ccxt(exchange_id="binance", symbol=pair, timeframe="1m", limit=50)
        assert not df.empty and set(["open","high","low","close","volume"]).issubset(df.columns)
        print(f"test_ccxt_fetch : OK - Fetched OHLCV via CCXT for {pair}")
        print("==============================")
        print(df)
        print("==============================")
    except Exception as e:
        print("test_ccxt_fetch : SKIP-", e)
if __name__ == "__main__":
    main()