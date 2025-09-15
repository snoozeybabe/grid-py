import asyncio
from src.dydx_connector import DYDXConnector

# Replace with your testnet wallet address
WALLET_ADDRESS = "dydx1zas7l8nq3c42gqv8lffd5d0n97xkqcf370k04j"

async def test_connection():
    connector = DYDXConnector(testnet=True)
    print("===== dYdX v4 Indexer API Test =====")

    # 1. Markets
    markets = await connector.get_markets()
    print("\nMarkets (first 5):")
    for i, (market, data) in enumerate(list(markets.items())[:5]):
        print(f" {i+1}. {market}: status={data.get('status')}")

    # 2. Candles
    candles = await connector.get_market_candles("ETH-USD", resolution="1H")
    print("\nETH-USD Candles (first 3):")
    for c in candles[:3]:
        print(c)

    # 3. Orderbook
    orderbook = await connector.get_orderbook("ETH-USD")
    print("\nETH-USD Orderbook:")
    print(" Asks:", orderbook.get("asks", [])[:2])
    print(" Bids:", orderbook.get("bids", [])[:2])

    # 4. Account Info
    account_info = await connector.get_account_info(WALLET_ADDRESS, 0)
    print("\nAccount Info:")
    print(account_info)

    # 5. Positions
    positions = await connector.get_positions(WALLET_ADDRESS, 0)
    print("\nPositions:")
    print(positions)

    print("\n=== Test Complete ===")

if __name__ == "__main__":
    asyncio.run(test_connection())
