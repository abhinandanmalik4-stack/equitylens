import unittest

import pandas as pd

from equitylens.catalog import INSTRUMENTS
from equitylens.providers import DemoProvider, validate_history


class ProviderTests(unittest.TestCase):
    def test_deterministic_and_explicitly_synthetic(self):
        provider = DemoProvider()
        a, b = [provider.history(INSTRUMENTS[0]) for _ in range(2)]
        pd.testing.assert_frame_equal(a.frame, b.frame)
        self.assertTrue(a.is_demo)
        self.assertEqual(str(a.as_of), "2026-10-23")
        self.assertEqual(len(a.frame), 252)

    def test_all_instruments_have_valid_different_paths(self):
        frames = [DemoProvider().history(i).frame for i in INSTRUMENTS]
        self.assertEqual(len({tuple(f.close) for f in frames}), len(INSTRUMENTS))

    def test_reject_bad_data(self):
        original = DemoProvider().history(INSTRUMENTS[0]).frame
        for column, value in [("high", 1), ("close", float("nan")), ("volume", -1), ("volume", 1.5), ("date", pd.NaT)]:
            with self.subTest(column=column, value=value):
                invalid = original.copy()
                if column == "volume":
                    invalid["volume"] = invalid["volume"].astype(float)
                invalid.loc[0, column] = value
                with self.assertRaises(ValueError):
                    validate_history(invalid)
        for bad in [original.iloc[::-1], pd.concat([original, original.iloc[[-1]]]), original.iloc[:0]]:
            with self.assertRaises(ValueError):
                validate_history(bad)


if __name__ == "__main__":
    unittest.main()
