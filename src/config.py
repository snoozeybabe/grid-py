from dataclasses import dataclass

@dataclass

class GridConfig:
    ema_len: int = 50
    atr_len: int = 14
    levels_each_side: int = 5
    step_k: float = 0.6
    min_step : float = 0.0
    recenter_k : float = 1.5
    atr_hysteresis: float = 0.25
    stop_steps: float = 3.0
    allow_shorts : bool = False
    size : float = 0.001
    cash : float = 10000.0
    commission_bps : float = 2.0
