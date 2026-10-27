"""Past-observation calculations. No predictions or live-quote assumptions."""

from dataclasses import dataclass

import pandas as pd

from equitylens.providers import validate_history

RANGES = {"1M": 21, "3M": 63, "6M": 126, "1Y": 252, "All": None}


@dataclass(frozen=True)
class Summary:
    latest: float
    previous: float | None
    change: float | None
    change_pct: float | None
    volume: int
    range_return_pct: float | None


def range_history(frame: pd.DataFrame, selected: str) -> pd.DataFrame:
    if selected not in RANGES:
        raise ValueError("Unsupported history range.")
    frame = validate_history(frame)
    count = RANGES[selected]
    return frame.tail(count).copy() if count else frame.copy()


def summarize(full_history: pd.DataFrame, visible: pd.DataFrame) -> Summary:
    full = validate_history(full_history)
    visible = validate_history(visible)
    latest = float(full.close.iloc[-1])
    previous = float(full.close.iloc[-2]) if len(full) > 1 else None
    change = latest - previous if previous is not None else None
    first, last = float(visible.close.iloc[0]), float(visible.close.iloc[-1])
    return Summary(
        latest, previous, change,
        100 * change / previous if previous is not None else None,
        int(full.volume.iloc[-1]),
        100 * (last / first - 1) if len(visible) > 1 else None,
    )


def normalized_comparison(a: pd.DataFrame, b: pd.DataFrame) -> pd.DataFrame:
    """Compare identical dates; both series start at 100 on first common date."""
    a, b = validate_history(a), validate_history(b)
    common = a[["date", "close"]].merge(b[["date", "close"]], on="date", suffixes=("_a", "_b"))
    if len(common) < 2:
        raise ValueError("Comparison needs at least two common dates.")
    for column in ("close_a", "close_b"):
        common[column] = 100 * common[column] / common[column].iloc[0]
    return common


def calendar_window(frame: pd.DataFrame, start, end) -> pd.DataFrame:
    """Inclusive date selection; return no rows for a window without observations."""
    frame = validate_history(frame)
    bounds = []
    for value in (start, end):
        if isinstance(value, (int, float, bool)):
            raise ValueError("Select explicit calendar dates.")
        stamp = pd.Timestamp(value)
        if pd.isna(stamp) or stamp.tzinfo is not None or stamp != stamp.normalize():
            raise ValueError("Range boundaries must be timezone-naive daily dates.")
        bounds.append(stamp)
    start, end = bounds
    if start > end:
        raise ValueError("Start date must not be after end date.")
    return frame.loc[frame.date.between(start, end)].copy().reset_index(drop=True)
