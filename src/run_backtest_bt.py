import argparse
import matplotlib.pyplot as plt
from backtesting.lib import FractionalBacktest

from src.data_utils import load_csv, fetch_ohlcv_ccxt, preprocess
from src.indicators_lib import add_indicators
from src.grid_strategy import GridScalperBT


def estimated_cash_needeed(df,levels_each_side, size, step_k=0.6):
    if df.empty:
        return 0
    price = df["Close"].iloc[-1] if "Close" in df else df["close"].iloc[-1]
    atr = df["ATR"].iloc[-1] if 'ATR' in df.columns else (price * 0.01)
    step = max(0.0001 * price, step_k * atr)
    buy_levels = [price - (i+1) * step for i in range(levels_each_side)]
    return sum(lv * size for lv in buy_levels)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv', type=str, default=None, help='Path to CSV file')
    parser.add_argument('--ccxt', action='store_true', help='Use CCXT to fetch data instead of csv')
    parser.add_argument("--exchange", type=str, default="bitget", help="Exchange to use for CCXT")
    parser.add_argument("--symbol", type=str, default="BTC/USDT", help="Symbol to use for CCXT")
    parser.add_argument("--timeframe", type=str, default="1m", help="Timeframe to use for CCXT")
    parser.add_argument("--limit", type=int,default=1000)
    parser.add_argument("--levels", type=int, default=5, help="Number of levels to use for grid")
    parser.add_argument("--step_k", type=float, default=0.6, help="Step size for grid")
    parser.add_argument("--min_step", type=float, default=0.0, help="Minimum step size for grid")
    parser.add_argument("--recenter_k", type=float, default=1.5, help="Recentering factor for grid")
    parser.add_argument("--atr_hyst", type=float, default=0.25, help="ATR hysteresis for grid")
    parser.add_argument("--stop_steps", type=float, default=3.0, help="Stop loss steps for grid")
    parser.add_argument("--allow_shorts", action="store_true", help="Allow shorts in grid")
    parser.add_argument("--size", type=float, default=0.001, help="Size of each trade")
    parser.add_argument("--cash", type=float, default=10000)
    parser.add_argument("--commission_bps", type=float, default=2.0)
    args = parser.parse_args()


    if args.ccxt:
        df = fetch_ohlcv_ccxt(exchange_id=args.exchange, symbol=args.symbol, timeframe=args.timeframe, limit=args.limit)
    elif args.csv:
        df = load_csv(args.csv)
        df = preprocess(df)
    else:
        raise ValueError("Provider --csv PATH or --ccxt with --exchange/--symbol/--timeframe")
    

    df = add_indicators(df, ema_len=50,atr_len=14)
    df_bt = df.rename(columns={"open":"Open","high":"High","low":"Low","close":"Close","volume":"Volume"})

    cash_needed = estimated_cash_needeed(df_bt, args.levels, args.size, args.step_k)
    if cash_needed > args.cash * 0.8:
        print(f"Warning : Estimated needed cash {cash_needed:.2f} is greater than 80% of cash available {args.cash:.2f}")
        print(f"Consider : --cash {int(cash_needed*1.5)} or --size {args.size*0.5:.6f} or --levels {max(1, args.levels-1)}")

    bt = FractionalBacktest(
        df_bt,
        GridScalperBT,
        cash=args.cash, 
        commission=args.commission_bps/10000.0,
        exclusive_orders=False
    )

    stats = bt.run(
        level_each_side=args.levels,
        step_k=args.step_k,
        min_step=args.min_step,
        recenter_k=args.recenter_k,
        atr_hysteresis=args.atr_hyst,
        stop_steps=args.stop_steps,
        allow_shorts=args.allow_shorts,
        size=args.size
    )

    print("Summary:")
    print(stats)

    try:
        bt.plot(open_browser=True)
        plt.show()
    except:
       pass

if __name__ == "__main__":
    main()
