"""Finite percentage arithmetic for validated, positive price observations."""

import math


def price_change_pct(latest: float, previous: float) -> float | None:
    latest, previous = float(latest), float(previous)
    if not math.isfinite(latest) or not math.isfinite(previous) or min(latest, previous) <= 0:
        raise ValueError("Price changes need finite, positive observations.")
    result = ((latest - previous) / previous) * 100
    return result if math.isfinite(result) else None
