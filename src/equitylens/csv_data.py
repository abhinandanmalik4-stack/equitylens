"""Bounded local OHLCV import. File content and source labels are unverified."""

import csv
from datetime import datetime
from io import StringIO
import re
from zoneinfo import ZoneInfo

import pandas as pd

from equitylens.catalog import Instrument
from equitylens.providers import OHLCV, PriceHistory

MAX_BYTES = 2 * 1024 * 1024
MAX_ROWS = 10_000
METADATA = {"instrument", "currency", "source", "is_demo", "adjustment"}


def import_history(raw: bytes, instrument: Instrument, source: str, adjustment: str, *, is_demo: bool = True) -> PriceHistory:
    if not isinstance(raw, bytes):
        raise ValueError("CSV input must be bytes read from a file.")
    if not isinstance(instrument, Instrument):
        raise ValueError("Select a valid Instrument before importing history.")
    if not isinstance(is_demo, bool):
        raise ValueError("The demo flag must be an explicit boolean.")
    if not raw or len(raw) > MAX_BYTES:
        raise ValueError("Provide a nonempty CSV no larger than 2 MiB.")
    if any(not isinstance(value, str) or not value.strip() or len(value) > 200 for value in (source, adjustment)):
        raise ValueError("Source and adjustment policy must each contain 1-200 characters.")
    try:
        text = raw.decode("utf-8-sig")
        reader = csv.reader(StringIO(text), strict=True)
        header = [value.strip().lower() for value in next(reader)]
        if len(header) != len(set(header)) or not set(OHLCV).issubset(header):
            raise ValueError("CSV needs unique date, open, high, low, close and volume columns.")
        if set(header) - set(OHLCV) - METADATA:
            raise ValueError("Unsupported CSV columns; convert to the documented EquityLens format.")
        rows = []
        for row in reader:
            if not row:
                continue
            if len(row) != len(header) or len(rows) >= MAX_ROWS:
                raise ValueError("CSV has a malformed row or exceeds 10,000 observations.")
            rows.append(row)
    except (UnicodeError, csv.Error, StopIteration) as exc:
        raise ValueError("CSV must be valid UTF-8 text with a comma-separated header.") from exc
    if not rows:
        raise ValueError("CSV has no observations.")
    frame = pd.DataFrame(rows, columns=header)
    for column, expected in (("instrument", instrument.key), ("currency", instrument.currency)):
        if column in frame and not frame[column].eq(expected).all():
            raise ValueError(f"CSV {column} does not match the selected company.")
    for column in ("source", "adjustment", "is_demo"):
        if column in frame and frame[column].nunique(dropna=False) != 1:
            raise ValueError(f"CSV {column} must be consistent across all rows.")
    if "is_demo" in frame:
        marker = frame.is_demo.iloc[0].strip().lower()
        if marker not in ("true", "false"):
            raise ValueError("CSV is_demo values must be True or False.")
        is_demo = is_demo or marker == "true"
    if not frame.date.map(lambda value: bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", value))).all():
        raise ValueError("CSV dates must be YYYY-MM-DD; convert ambiguous dates explicitly.")
    frame["date"] = pd.to_datetime(frame["date"], format="%Y-%m-%d", errors="raise")
    today = datetime.now(ZoneInfo("Asia/Kolkata")).date()
    if frame.date.max().date() > today:
        raise ValueError("Historical observations cannot contain future dates in India time.")
    return PriceHistory(
        instrument, frame, f"User supplied (unverified): {source.strip()}", is_demo,
        frame.date.iloc[-1].date(), adjustment.strip(),
    )
