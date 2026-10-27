"""Inspect a local CSV without launching the app or fetching any network data."""

import argparse
import json
from pathlib import Path
import sys

from equitylens.catalog import get_instrument
from equitylens.csv_data import MAX_BYTES, import_history
from equitylens.exports import dataset_id


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", type=Path)
    parser.add_argument("--instrument", required=True, help="For example NSE:RELIANCE")
    parser.add_argument("--source", required=True)
    parser.add_argument("--adjustment", required=True)
    parser.add_argument("--demo", action="store_true", help="Mark invented or example observations")
    args = parser.parse_args(argv)
    try:
        with args.csv.open("rb") as handle:
            raw = handle.read(MAX_BYTES + 1)
        history = import_history(raw, get_instrument(args.instrument), args.source, args.adjustment, is_demo=args.demo)
        report = {
            "valid_structure": True, "verification": "User-supplied data; not independently verified",
            "instrument": history.instrument.key, "currency": history.instrument.currency,
            "source": history.source, "is_demo": history.is_demo,
            "observations": len(history.frame), "first_date": str(history.frame.date.iloc[0].date()),
            "as_of": str(history.as_of), "adjustment": history.adjustment,
            "zero_volume_observations": int(history.frame.volume.eq(0).sum()),
            "largest_calendar_gap_days": int(history.frame.date.diff().dt.days.max()) if len(history.frame) > 1 else None,
            "dataset_sha256": dataset_id(history),
        }
    except (ValueError, TypeError, OSError) as exc:
        print(json.dumps({"valid_structure": False, "error": str(exc)}), file=sys.stderr)
        return 2
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
