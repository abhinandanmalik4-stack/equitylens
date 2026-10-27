"""Labelled CSV export with dataset identity and spreadsheet-safe metadata."""

from hashlib import sha256
import json

import pandas as pd

from equitylens.providers import PriceHistory, validate_history


def dataset_id(history: PriceHistory) -> str:
    metadata = json.dumps({
        "instrument": history.instrument.key, "currency": history.instrument.currency,
        "source": history.source, "is_demo": history.is_demo,
        "as_of": str(history.as_of), "adjustment": history.adjustment,
    }, sort_keys=True)
    return sha256((metadata + history.frame.to_csv(index=False, date_format="%Y-%m-%d")).encode()).hexdigest()


def _safe_text(value: str) -> str:
    return "'" + value if value.lstrip().startswith(("=", "+", "-", "@")) else value


def export_history(history: PriceHistory, frame: pd.DataFrame | None = None) -> bytes:
    visible = validate_history(history.frame if frame is None else frame)
    original = validate_history(history.frame).set_index("date")
    candidate = visible.set_index("date")
    if not candidate.index.isin(original.index).all() or not candidate.eq(original.loc[candidate.index]).all().all():
        raise ValueError("Export rows must belong to the labelled source history.")
    exported = visible.assign(
        instrument=_safe_text(history.instrument.key), currency=_safe_text(history.instrument.currency),
        source=_safe_text(history.source), is_demo=history.is_demo,
        adjustment=_safe_text(history.adjustment),
    )
    return exported.to_csv(index=False, date_format="%Y-%m-%d").encode("utf-8")
