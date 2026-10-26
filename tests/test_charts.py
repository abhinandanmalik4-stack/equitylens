import unittest

from equitylens.catalog import INSTRUMENTS
from equitylens.charts import comparison_figure, price_figure
from equitylens.providers import DemoProvider


class ChartTests(unittest.TestCase):
    def test_both_chart_types_keep_volume_and_observation_count(self):
        frame = DemoProvider().history(INSTRUMENTS[0]).frame.tail(21)
        for kind in ("Line", "Candlestick"):
            fig = price_figure(frame, "INR", kind)
            self.assertEqual(len(fig.data[0].x), 21)
            self.assertEqual(fig.data[1].type, "bar")
            self.assertEqual(list(fig.data[1].y), frame.volume.tolist())
            fig.to_json()

    def test_comparison_starts_at_equal_base(self):
        a, b = [DemoProvider().history(i).frame for i in INSTRUMENTS[:2]]
        fig = comparison_figure(a, b, ("RELIANCE", "TCS"))
        self.assertEqual([trace.y[0] for trace in fig.data], [100, 100])


if __name__ == "__main__":
    unittest.main()
