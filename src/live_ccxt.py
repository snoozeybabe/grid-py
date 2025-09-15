import os
import time
import math
import pandas as pd
import pandas_ta as ta
import ccxt

from dotenv import load_dotenv

load_dotenv()

LIVE = False
EXCHANCE_ID="bitget"
SYMBOL="XRP/USDT:USDT"
TIMEFRAME="1m"
LEVEL_EACH_SIDE=4
STEP_K=0.6
STOP_STEPS=3.0
SIZE=0.001

def round_to(value, step):
    return math.floor(value / step) * step

def compute_grid(df : pd.DataFrame, levels_each_side=LEVEL_EACH_SIDE, step_k=STEP_K, stop_steps=STOP_STEPS):
    ema = ta.ema(df["close"], length=50).iloc[-1]
    atr = ta.atr(df["high"], df["low"], df["close"], length=14).iloc[-1]
    step = max(1e-9,step_k * atr)
    buys = [ema - (i+1) * step for i in range(levels_each_side)]
    sells = [ema + (i+1) * step for i in range(levels_each_side)]
    return ema,atr,step,buys, sells

def fetch_latest_df(ex,symbol=SYMBOL,timeframe=TIMEFRAME,limit=100):
    ohlcv = ex.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms",utc=True)
    df = df.set_index("timestamp").sort_index()
    return df

def main():

    print("======Vars========")
    print(os.getenv("BITGET_API_KEY"))
    print("======Vars========")
    
    #ex = getattr(ccxt,EXCHANCE_ID)({"enableRateLimit" : True, "apiKey": os.getenv("BITGET_API_KEY"), "secret": os.getenv("BITGET_API_SECRET"), "password": os.getenv("BITGET_API_PASSPHRASE")})
    ex = ccxt.bitget({
        "enableRateLimit": True,
        "apiKey": os.getenv("BITGET_API_KEY"),
        "secret": os.getenv("BITGET_API_SECRET"),
        "password": os.getenv("BITGET_API_PASSPHRASE"),
        "options" : {
            "defaultType": "swap"
        }
    })
    # ex.set_sandbox_mode(True)  # Uncomment if supported and you want testnet
    # ex.apiKey, ex.secret = os.getenv("API_KEY"), os.getenv("API_SECRET")  # Ensure keys set if LIVE
    print("Here")


    print("===========Account infos==========")
    print(f"Balance = {ex.fetch_balance()}")
    #print(f"Maket : {ex.fetch_markets()}")
    print("==================================")
    while True:
        try:
            df =fetch_latest_df(ex,SYMBOL,TIMEFRAME,limit=100)
            ema,atr,step,buys,sells = compute_grid(df)
            last = df["close"].iloc[-1]

            market = ex.market(SYMBOL)
            price_step = market.get("precision",{}).get("price",None)
            amount_step = market.get("precision",{}).get("amount",None)

            def rprice(p): return round(p,price_step) if isinstance(price_step,int) else p
            def ramount(a): return round(a,amount_step) if isinstance(amount_step,int) else a

            qty = SIZE
            print(f"Last={last:.2f} EMA={ema:.2f} ATR={atr:.2f} Step={step:.2f} Qty={qty:.6f}")
            for lv in buys:
                p = rprice(lv)
                print(f"Plan BUY limit at {p}, qty={qty}")
                ex.create_order(SYMBOL, type="limit", side="buy", price='2.9600', amount='2')
                if LIVE:
                    try:
                        ex.create_order(SYMBOL, type="limit", side="buy", price=p, amount=qty)
                    except Exception as e:
                        print(f"Error placing buy order: {e}")
            # Optional short side if enabled in your account
            # for lv in sells:
            #     p = rprice(lv)
            #     print(f"Plan SELL limit at {p}, qty={qty}")
            #     if LIVE:
            #         ex.create_order(SYMBOL, type="limit", side="sell", amount=qty, price=p)

            time.sleep(60)  # Wait for 1 minute before next update
        except Exception as e:
            print(f"Error in main loop: {e}")
            time.sleep(10)  # Brief pause before retry

if __name__ == "__main__":
    main()
