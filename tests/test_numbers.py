import unittest

import pandas as pd

from equitylens.analytics import normalized_comparison, summarize
from equitylens.numbers import price_change_pct
from equitylens.performance import historical_returns


def observations(prices):
    return pd.DataFrame({"date": pd.date_range("2026-01-01", periods=len(prices)),
                         "open": prices, "high": prices, "low": prices, "close": prices, "volume": 1})


class NumericBoundaryTests(unittest.TestCase):
    def test_normal_and_large_unchanged_prices(self):
        self.assertAlmostEqual(price_change_pct(99, 110), -10)
        self.assertEqual(price_change_pct(1e308, 1e308), 0)
        frame = observations([1e308, 1e308])
        self.assertEqual(normalized_comparison(frame, frame).close_a.tolist(), [100, 100])

    def test_unrepresentable_returns_are_unavailable_not_infinity(self):
        self.assertIsNone(price_change_pct(1e308, 1e-300))
        frame = observations([1e-300, 1e308])
        self.assertIsNone(summarize(frame, frame).change_pct)
        self.assertIsNone(summarize(frame, frame).range_return_pct)
        self.assertTrue(pd.isna(historical_returns(frame).loc[0, "Price change (%)"]))
        with self.assertRaises(ValueError):
            normalized_comparison(frame, frame)

    def test_invalid_price_inputs_are_not_coerced_to_a_result(self):
        for value in (0, -1, float("nan"), float("inf")):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    price_change_pct(value, 100)


if __name__ == "__main__":
    unittest.main()
