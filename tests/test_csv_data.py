import unittest

from equitylens.catalog import INSTRUMENTS
from equitylens.csv_data import MAX_BYTES, MAX_ROWS, import_history

CSV = b"date,open,high,low,close,volume\n2026-01-02,100,112,98,110,1000\n2026-01-05,110,115,105,108,900\n"


class CsvImportTests(unittest.TestCase):
    def load(self, raw=CSV, **kwargs):
        return import_history(raw, INSTRUMENTS[0], "My local file", "Unadjusted", **kwargs)

    def test_default_is_demo_and_non_demo_remains_unverified(self):
        self.assertTrue(self.load().is_demo)
        result = self.load(is_demo=False)
        self.assertFalse(result.is_demo)
        self.assertIn("unverified", result.source)
        self.assertEqual(result.frame.close.tolist(), [110, 108])

    def test_bom_and_padded_header(self):
        raw = b"\xef\xbb\xbf" + CSV.replace(b"date,open", b" Date , Open ", 1)
        self.assertEqual(len(self.load(raw).frame), 2)

    def test_invalid_argument_types_produce_controlled_errors(self):
        defaults = dict(raw=CSV, instrument=INSTRUMENTS[0], source="Local file", adjustment="Unadjusted", is_demo=True)
        invalid = {"raw": [None, CSV.decode(), bytearray(CSV)],
                   "instrument": [None, "NSE:RELIANCE"],
                   "source": [None, 42, " ", "x" * 201],
                   "adjustment": [None, 42, " ", "x" * 201],
                   "is_demo": [None, 0, 1, "False", "True"]}
        for argument, values in invalid.items():
            for value in values:
                with self.subTest(argument=argument, value=repr(value)[:30]):
                    with self.assertRaises(ValueError):
                        import_history(**(defaults | {argument: value}))

    def test_row_limit_is_enforced_before_history_validation(self):
        header, first, _ = CSV.decode().splitlines()
        oversized = (header + "\n" + (first + "\n") * (MAX_ROWS + 1)).encode()
        self.assertLess(len(oversized), MAX_BYTES)
        with self.assertRaisesRegex(ValueError, "10,000"):
            self.load(oversized)

    def test_inconsistent_and_unknown_demo_markers_are_rejected(self):
        header, first, second = CSV.decode().splitlines()
        for markers in (("True", "False"), ("yes", "yes"), ("", "")):
            with self.subTest(markers=markers):
                raw = f"{header},is_demo\n{first},{markers[0]}\n{second},{markers[1]}\n".encode()
                with self.assertRaises(ValueError):
                    self.load(raw)

    def test_bad_files_fail_closed(self):
        bad_files = [b"", b"x" * (MAX_BYTES + 1), b"\xff", CSV.replace(b"date,open", b"date,date"),
                     CSV.replace(b"2026-01-02", b"01/02/2026"), CSV.replace(b"2026-01-05", b"2999-01-05"),
                     CSV.replace(b"1000", b"1000,extra"), CSV.replace(b"date,open", b"date,unknown")]
        for raw in bad_files:
            with self.subTest(prefix=raw[:30]):
                with self.assertRaises(ValueError):
                    self.load(raw)

    def test_volume_fraction_is_rejected_before_rounding(self):
        for volume in (b"1.0000000000000000001", b"-1e-400"):
            with self.subTest(volume=volume):
                with self.assertRaisesRegex(ValueError, "whole number"):
                    self.load(CSV.replace(b"1000", volume))
        self.assertEqual(self.load(CSV.replace(b"1000", b"1e3")).frame.volume.iloc[0], 1000)

    def test_identity_mismatch_and_demo_marker_cannot_be_erased(self):
        tagged = CSV.decode().splitlines()
        raw = (tagged[0] + ",instrument,currency,is_demo\n" + "\n".join(row + ",NSE:RELIANCE,INR,True" for row in tagged[1:])).encode()
        self.assertTrue(self.load(raw, is_demo=False).is_demo)
        with self.assertRaises(ValueError):
            self.load(raw.replace(b"NSE:RELIANCE", b"NSE:TCS"))


if __name__ == "__main__":
    unittest.main()
