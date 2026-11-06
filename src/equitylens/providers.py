"""Provider contract and reproducible synthetic fixtures; no market-data calls."""

from dataclasses import dataclass
from datetime import date
from hashlib import sha256
from typing import Protocol

import numpy as np
import pandas as pd

from equitylens.catalog import Instrument

OHLCV = ("date", "open", "high", "low", "close", "volume")


def validate_history(frame: pd.DataFrame) -> pd.DataFrame:
    """Reject ambiguous/bad data rather than silently inventing replacements."""
    if not isinstance(frame, pd.DataFrame):
        raise ValueError("History must be a pandas DataFrame.")
    if frame.empty or not set(OHLCV).issubset(frame.columns):
        raise ValueError("History must contain dated OHLCV rows.")
    if not frame.columns.is_unique:
        raise ValueError("History column names must be unique.")
    data = frame.loc[:, list(OHLCV)].copy()
    if pd.api.types.is_numeric_dtype(data["date"]) or data["date"].map(lambda v: isinstance(v, (int, float, bool))).any():
        raise ValueError("Dates must be explicit daily dates, not numbers or booleans.")
    data["date"] = pd.to_datetime(data["date"], errors="raise")
    if data["date"].isna().any() or data["date"].dt.tz is not None:
        raise ValueError("Daily dates must be valid timezone-naive session labels.")
    if not data["date"].equals(data["date"].dt.normalize()):
        raise ValueError("Daily history must use dates, not intraday timestamps.")
    if data["date"].duplicated().any() or not data["date"].is_monotonic_increasing:
        raise ValueError("Daily dates must be unique and increasing.")
    for column in OHLCV[1:]:
        if data[column].dtype.kind in {"M", "m"}:
            raise ValueError(f"{column} must contain numbers, not dates or durations.")
        if data[column].map(lambda v: isinstance(v, (bool, np.bool_))).any():
            raise ValueError(f"{column} must contain numbers, not booleans.")
        data[column] = pd.to_numeric(data[column], errors="raise")
        if pd.api.types.is_complex_dtype(data[column]):
            raise ValueError(f"{column} must contain real numbers.")
    values = data[list(OHLCV[1:])].to_numpy(dtype=float)
    if not np.isfinite(values).all():
        raise ValueError("OHLCV values must be finite.")
    if (data[["open", "high", "low", "close"]] <= 0).any().any():
        raise ValueError("Prices must be positive.")
    if (data["volume"] < 0).any() or (data["volume"] % 1 != 0).any():
        raise ValueError("Volume must be a nonnegative whole number.")
    if (data["high"] < data[["open", "close", "low"]].max(axis=1)).any():
        raise ValueError("High cannot be below open, close or low.")
    if (data["low"] > data[["open", "close", "high"]].min(axis=1)).any():
        raise ValueError("Low cannot be above open, close or high.")
    return data.reset_index(drop=True)


@dataclass
class PriceHistory:
    instrument: Instrument
    frame: pd.DataFrame
    source: str
    is_demo: bool
    as_of: date
    adjustment: str

    def __post_init__(self):
        if not isinstance(self.instrument, Instrument):
            raise ValueError("History must identify an Instrument.")
        if not isinstance(self.is_demo, bool):
            raise ValueError("The demo flag must be an explicit boolean.")
        if any(not isinstance(value, str) or not value.strip() for value in (self.source, self.adjustment)):
            raise ValueError("Source and price adjustment policy are required.")
        self.frame = validate_history(self.frame)
        if self.frame["date"].iloc[-1].date() != self.as_of:
            raise ValueError("As-of date must match the last available session.")


class PriceProvider(Protocol):
    def history(self, instrument: Instrument) -> PriceHistory: ...


class DemoProvider:
    """252 weekday observations, ending on a fixed past date, not trading sessions.

    Prices, volumes and price paths are invented. Weekday dates intentionally do
    not model exchange holidays or corporate actions. No claims of live data.
    """

    def history(self, instrument: Instrument) -> PriceHistory:
        seed = int.from_bytes(sha256(instrument.key.encode()).digest()[:4], "big")
        rng = np.random.default_rng(seed)
        dates = pd.bdate_range(end="2026-10-23", periods=252)
        base = 500 + seed % 2500
        close = base * np.exp(np.cumsum(rng.normal(0.0006, 0.012, len(dates))))
        opening = np.r_[base, close[:-1]] * (1 + rng.normal(0, 0.003, len(dates)))
        high = np.maximum(opening, close) * (1 + rng.uniform(0.001, 0.015, len(dates)))
        low = np.minimum(opening, close) * (1 - rng.uniform(0.001, 0.015, len(dates)))
        frame = pd.DataFrame({
            "date": dates, "open": opening.round(2), "high": high.round(2),
            "low": low.round(2), "close": close.round(2),
            "volume": rng.integers(100_000, 5_000_000, len(dates)),
        })
        return PriceHistory(
            instrument, frame, "EquityLens synthetic fixture v1", True,
            dates[-1].date(), "Synthetic; no corporate-action adjustment",
        )
