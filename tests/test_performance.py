import unittest

import pandas as pd

from equitylens.performance import historical_returns, max_drawdown_pct


def frame(prices):
    return pd.DataFrame({"date": pd.date_range("2026-01-01", periods=len(prices)), "open": prices,
                         "high": prices, "low": prices, "close": prices, "volume": 1})


class PerformanceTests(unittest.TestCase):
    def test_drawdown_uses_running_peak_not_first_price(self):
        self.assertAlmostEqual(max_drawdown_pct(frame([100, 120, 90, 110])), -25)
        self.assertEqual(max_drawdown_pct(frame([100, 110, 120])), 0)
        self.assertIsNone(max_drawdown_pct(frame([100])))

    def test_five_intervals_require_six_observations(self):
        short = historical_returns(frame([100] * 5))
        self.assertTrue(pd.isna(short.loc[1, "Price change (%)"]))
        complete = historical_returns(frame([100, 100, 100, 100, 100, 110]))
        self.assertAlmostEqual(complete.loc[1, "Price change (%)"], 10)
        self.assertEqual(str(complete.loc[1, "Start date"]), "2026-01-01")


if __name__ == "__main__":
    unittest.main()
