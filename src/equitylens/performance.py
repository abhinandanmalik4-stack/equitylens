"""Descriptive past-price statistics, not forecasts or total returns."""

import pandas as pd

from equitylens.numbers import price_change_pct
from equitylens.providers import validate_history

HORIZONS = {"Previous observation": 1, "5 intervals": 5, "21 intervals": 21, "63 intervals": 63, "126 intervals": 126}


def historical_returns(frame: pd.DataFrame) -> pd.DataFrame:
    frame = validate_history(frame)
    close = frame.close
    rows = []
    for label, intervals in HORIZONS.items():
        available = len(close) > intervals
        rows.append({
            "Period": label,
            "Start date": frame.date.iloc[-intervals - 1].date() if available else None,
            "End date": frame.date.iloc[-1].date(),
            "Price change (%)": price_change_pct(close.iloc[-1], close.iloc[-intervals - 1]) if available else None,
        })
    return pd.DataFrame(rows)


def max_drawdown_pct(frame: pd.DataFrame) -> float | None:
    frame = validate_history(frame)
    if len(frame) < 2:
        return None
    return float(((frame.close / frame.close.cummax()) - 1).min() * 100)
