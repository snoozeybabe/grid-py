from backtesting import Strategy
from typing import List
import numpy as np

class GridScalperBT(Strategy):

    #Need to add shorts if we use leverage
    level_each_side : int = 5
    step_k: float = 0.6
    min_step: float = 0.0
    recenter_k: float = 1.5
    atr_hysteresis: float = 0.25
    stop_steps: float = 3.0
    allow_shorts = False
    size = 0.001

    #internal State
    center_ref : float
    step_ref : float 
    atr_ref : float 
    open_orders : List

    def init(self):
        self.center_ref = np.nan
        self.step_ref = np.nan
        self.atr_ref = np.nan
        self.open_orders = []
    
    def _compute_step(self, atr : float) -> float:
        return max(self.min_step, self.step_k * max(1e-12,atr))

    def _build_levels(self, center : float, step : float):
        buys = [center - (i+1) * step for i in range(self.level_each_side)]
        sells = [center + (i+1) * step for i in range(self.level_each_side)]
        return buys, sells
    
    def _cancel_all(self):
        for o in list(self.open_orders):
            try:
                o.cancel()
            except Exception:
                pass
        self.open_orders.clear()
    
    def _place_grid(self, center : float, step : float):
        buys, sells = self._build_levels(center, step)
        price = float(self.data.Close[-1])
        available_cash = self._broker._cash
        total_cost_estimate = sum(lv* self.size for lv in buys)
        if available_cash * 0.9 < total_cost_estimate:
            print(f"Insufficient cash: need ~${total_cost_estimate:.0f}, have ${available_cash:.0f}")
            return
        for lv in buys:
            tp = lv + step * self.stop_steps
            sl = lv - (self.stop_steps * step) if self.stop_steps else None
            order_size = abs(self.size)
            if order_size * lv < 1.0:
                continue
            o = self.buy(size=order_size, limit=lv, tp=tp,sl=sl)
            self.open_orders.append(o)
        if self.allow_shorts:
            for lv in sells:
                tp = lv - step 
                sl = lv + (self.stop_steps * step) if self.stop_steps else None
                order_size = abs(self.size)
                if order_size * lv < 1.0:
                    continue
                o = self.sell(size=order_size, limit=lv, tp=tp,sl=sl)
                self.open_orders.append(o)
    def _should_recenter(self,price : float, center : float, atr : float) -> bool:
        if np.isnan(self.center_ref):
            return True
        step = max(1e12,self.step_ref)
        drift_steps = abs(price - self.center_ref) / step
        atr_change = abs(atr - self.atr_ref) / max(1e-12,self.atr_ref)
        return (drift_steps > self.recenter_k) or (atr_change > self.atr_hysteresis)
    
    def next(self):
        price = float(self.data.Close[-1])
        ema = float(self.data.EMA[-1]) if hasattr(self.data,"EMA") else np.nan
        atr = float(self.data.ATR[-1]) if hasattr(self.data,"ATR") else np.nan
        if np.isnan(ema) or np.isnan(atr) or atr <= 0:
            return

        center = ema 
        step = self._compute_step(atr)

        if self._should_recenter(price,center,atr):
            self._cancel_all()
            self.center_ref = center
            self.step_ref = step
            self.atr_ref = atr
            self._place_grid(self.center_ref,self.step_ref)
