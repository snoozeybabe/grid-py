import asyncio
from dydx_v4_client.indexer.rest.indexer_client import IndexerClient
from dydx_v4_client.network import make_testnet, make_mainnet


class DYDXConnector:
    def __init__(self, testnet: bool = True):
        """
        Initialize the dYdX v4 Indexer client.
        """
        self.network = make_testnet() if testnet else make_mainnet()
        self.client = IndexerClient(self.network.rest_indexer)
        print(f"Connected to dYdX {'testnet' if testnet else 'mainnet'} Indexer API")

    # ---------------------------
    # Account & Subaccount Queries
    # ---------------------------
    async def get_account_info(self, address: str, subaccount_number: int = 0):
        try:
            subaccount = await self.client.account.get_subaccount(address, subaccount_number)
            return subaccount.get("subaccount", {})
        except Exception as e:
            print(f"Error fetching account info: {e}")
            return {}

    async def get_positions(self, address: str, subaccount_number: int = 0):
        try:
            positions = await self.client.account.get_subaccount_perpetual_positions(
                address, subaccount_number
            )
            return positions.get("positions", [])
        except Exception as e:
            print(f"Error fetching positions: {e}")
            return []

    # ---------------------------
    # Market Data
    # ---------------------------
    async def get_markets(self):
        try:
            markets = await self.client.markets.get_perpetual_markets()
            return markets.get("markets", {})
        except Exception as e:
            print(f"Error fetching markets: {e}")
            return {}

    async def get_market_candles(self, market: str = "ETH-USD", resolution: str = "1m"):
        try:
            candles = await self.client.markets.get_perpetual_market_candles(
                market=market,
                resolution=resolution
            )
            return candles.get("candles", [])
        except Exception as e:
            print(f"Error fetching market data: {e}")
            return []

    async def get_orderbook(self, market: str = "ETH-USD"):
        try:
            orderbook = await self.client.markets.get_perpetual_market_orderbook(market)
            return orderbook
        except Exception as e:
            print(f"Error fetching orderbook: {e}")
            return {}

    async def get_trades(self, market: str = "ETH-USD"):
        try:
            trades = await self.client.markets.get_perpetual_market_trades(market)
            return trades.get("trades", [])
        except Exception as e:
            print(f"Error fetching trades: {e}")
            return []
