import unittest

import pandas as pd

from equitylens.analytics import normalized_comparison, range_history, summarize


def fixture(prices=(100, 110, 99), start="2026-01-01"):
    return pd.DataFrame({
        "date": pd.date_range(start, periods=len(prices)), "open": prices,
        "high": prices, "low": prices, "close": prices, "volume": 1000,
    })


class AnalyticsTests(unittest.TestCase):
    def test_previous_session_not_range_start(self):
        full = fixture()
        result = summarize(full, full.iloc[-2:])
        self.assertEqual(result.previous, 110)
        self.assertEqual(result.change, -11)
        self.assertAlmostEqual(result.change_pct, -10)
        self.assertAlmostEqual(result.range_return_pct, -10)

    def test_single_observation_does_not_invent_previous_price(self):
        result = summarize(fixture((100,)), fixture((100,)))
        self.assertIsNone(result.change_pct)
        self.assertIsNone(result.range_return_pct)

    def test_range_is_observation_count_not_calendar_month(self):
        self.assertEqual(len(range_history(fixture(tuple(range(1, 41))), "1M")), 21)
        with self.assertRaises(ValueError):
            range_history(fixture(), "1D")

    def test_comparison_uses_common_dates_and_rebases(self):
        result = normalized_comparison(fixture(), fixture((200, 220), start="2026-01-02"))
        self.assertEqual(len(result), 2)
        self.assertEqual(result.close_a.iloc[0], 100)
        self.assertEqual(result.close_b.iloc[0], 100)
        self.assertAlmostEqual(result.close_a.iloc[-1], 90)
        self.assertAlmostEqual(result.close_b.iloc[-1], 110)
        with self.assertRaises(ValueError):
            normalized_comparison(fixture(), fixture(start="2025-01-01"))


if __name__ == "__main__":
    unittest.main()
