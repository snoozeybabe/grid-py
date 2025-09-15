import os
import ccxt



from dotenv import load_dotenv

load_dotenv()

def test_bitget_connection():
    # Initialize Bitget client with API credentials from env variables
    bitget = ccxt.bitget({
        'apiKey': os.getenv("BITGET_API_KEY"),
        'secret': os.getenv("BITGET_API_SECRET"),
        'password': os.getenv("BITGET_API_PASSPHRASE"),
        'enableRateLimit': True,
        # Use swap to test futures
        'options': {
            'defaultType': 'swap',
        },
    })

    print("===== Bitget API Test =====")

    try:
        # 1. Fetch Markets
        markets = bitget.load_markets()
        print("\nMarkets (first 5):")
        for i, symbol in enumerate(list(markets.keys())[:5]):
            market = markets[symbol]
            status = market.get('info', {}).get('status', 'unknown')
            print(f" {i+1}. {symbol}: status={status}")

        # 2. Fetch OHLCV Candles for BTC/USDT swap
        candles = bitget.fetch_ohlcv('BTC/USDT:USDT', timeframe='1h', limit=3)
        print("\nBTC/USDT:USDT Candles (first 3):")
        for c in candles:
            print(c)

        # 3. Fetch Orderbook
        orderbook = bitget.fetch_order_book('BTC/USDT:USDT')
        print("\nBTC/USDT:USDT Orderbook (Top 2):")
        print(" Asks:", orderbook['asks'][:2])
        print(" Bids:", orderbook['bids'][:2])

        print("API_KEY:", os.getenv("BITGET_API_KEY"))
        print("SECRET:", os.getenv("BITGET_SECRET"))
        print("PASSWORD:", os.getenv("BITGET_PASSWORD"))
        # 4. Fetch Balance (USDT swap/futures)
        balance = bitget.fetch_balance()


        print("\nTotal Balance:")
        print(balance)
        usdt_balance = balance.get('USDT', {})
        print("\nUSDT Futures Balance:")
        print(usdt_balance)

        # 5. Fetch Open Positions for swap markets (if supported)
        # Bitget may require separate endpoints for positions — here is a common method:
        try:
            positions = bitget.fetch_positions()
            print("\nOpen Positions:")
            for pos in positions:
                print(pos)
        except Exception as e:
            print("Positions fetch not supported or failed:", e)

    except Exception as e:
        print("API Test failed with error:", e)

    print("\n=== Bitget Test Complete ===")

if __name__ == "__main__":
    test_bitget_connection()
