from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
import json
from pathlib import Path
import tempfile
import unittest

from equitylens.inspect_data import main


class InspectDataTests(unittest.TestCase):
    def test_reports_coverage_and_never_claims_verification(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "input.csv"
            path.write_text("date,open,high,low,close,volume\n2026-01-02,100,100,100,100,0\n2026-01-05,110,110,110,110,1\n", encoding="utf-8")
            output = StringIO()
            args = [str(path), "--instrument", "NSE:RELIANCE", "--source", "Local file", "--adjustment", "Unknown", "--demo"]
            with redirect_stdout(output):
                self.assertEqual(main(args), 0)
            report = json.loads(output.getvalue())
            self.assertEqual(report["largest_calendar_gap_days"], 3)
            self.assertEqual(report["zero_volume_observations"], 1)
            self.assertIn("not independently verified", report["verification"])
            self.assertTrue(report["is_demo"])

    def test_missing_file_returns_actionable_failure(self):
        with tempfile.TemporaryDirectory() as folder:
            error = StringIO()
            with redirect_stderr(error):
                code = main([str(Path(folder) / "missing.csv"), "--instrument", "NSE:RELIANCE", "--source", "File", "--adjustment", "Unknown"])
            self.assertEqual(code, 2)
            self.assertFalse(json.loads(error.getvalue())["valid_structure"])


if __name__ == "__main__":
    unittest.main()
