import os
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from streamlit.testing.v1 import AppTest

from equitylens.watchlist import Watchlist

APP = Path(__file__).resolve().parents[1] / "app.py"


class AppTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.db = Path(self.directory.name) / "watchlist.db"
        self.env = patch.dict(os.environ, {"EQUITYLENS_DB_PATH": str(self.db)})
        self.env.start()
        self.addCleanup(self.env.stop)

    def start(self):
        app = AppTest.from_file(str(APP), default_timeout=20).run()
        self.assertFalse(app.exception)
        return app

    def test_launch_has_clear_demo_notice(self):
        app = self.start()
        self.assertIn("invented demonstration data", app.warning[0].value)
        self.assertIn("Reliance Industries", [title.value for title in app.title])
        self.assertEqual(len(app.metric), 4)
        self.assertTrue(any("No trained model" in c.value for c in app.caption))

    def test_search_and_empty_state(self):
        app = self.start()
        app.text_input(key="search_query").set_value("infosys").run()
        self.assertFalse(app.exception)
        self.assertIn("Infosys", [title.value for title in app.title])
        app.text_input(key="search_query").set_value("no-such-company").run()
        self.assertFalse(app.exception)
        self.assertTrue(any("No matching companies" in i.value for i in app.info))
        self.assertEqual(len(app.metric), 0)

    def test_watchlist_survives_new_session_then_removes(self):
        app = self.start()
        app.button(key="watchlist_action").click().run()
        self.assertFalse(app.exception)
        self.assertEqual(Watchlist(self.db).items(), ["NSE:RELIANCE"])
        fresh = self.start()
        self.assertEqual(fresh.button(key="watchlist_action").label, "Remove from watchlist")
        fresh.button(key="watchlist_action").click().run()
        self.assertFalse(fresh.exception)
        self.assertEqual(Watchlist(self.db).items(), [])

    def test_saved_company_remains_accessible_after_search_miss(self):
        Watchlist(self.db).add("NSE:TCS")
        app = self.start()
        app.text_input(key="search_query").set_value("no-such-company").run()
        self.assertFalse(app.exception)
        self.assertTrue(app.button(key="watchlist_action").disabled)
        app.button(key="open:NSE:TCS").click().run()
        self.assertFalse(app.exception)
        self.assertIn("Tata Consultancy Services", [t.value for t in app.title])

    def test_ranges_chart_type_and_comparison(self):
        app = self.start()
        app.segmented_control(key="period").set_value("1M").run()
        app.segmented_control(key="chart_type").set_value("Candlestick").run()
        app.toggle(key="show_data").set_value(True).run()
        self.assertFalse(app.exception)
        self.assertEqual(len(app.dataframe[0].value), 21)
        app.selectbox(key="peer:NSE:RELIANCE").select("NSE:TCS").run()
        self.assertFalse(app.exception)
        self.assertEqual(len(app.get("plotly_chart")), 2)

    def test_storage_failure_does_not_break_charts(self):
        with patch.dict(os.environ, {"EQUITYLENS_DB_PATH": str(self.directory.name)}):
            app = self.start()
            self.assertTrue(app.button(key="watchlist_action").disabled)
            self.assertEqual(len(app.metric), 4)

    def test_upload_is_company_scoped_and_bad_replacement_clears_chart(self):
        raw = b"date,open,high,low,close,volume\n2026-01-02,100,110,100,110,1000\n2026-01-05,110,110,108,108,900\n"
        upload = SimpleNamespace(getvalue=lambda: raw)
        # AppTest cannot drive the browser's file picker. Mock only that boundary;
        # exercise the actual form, parser, state, metrics and chart code.
        with patch("streamlit.file_uploader", return_value=upload):
            app = self.start()
            app.segmented_control(key="data_mode").set_value("CSV upload").run()
            self.assertEqual(len(app.metric), 0)
            app.text_input(key="source:NSE:RELIANCE").set_value("Local test fixture")
            app.checkbox(key="demo:NSE:RELIANCE").uncheck()
            app.form_submit_button(key="load_csv").click().run()
            self.assertFalse(app.exception)
            self.assertEqual(app.metric[0].value, "108.00")
            self.assertTrue(any("unverified" in item.value for item in app.warning))
            self.assertFalse(any(s.label == "Compare with" for s in app.selectbox))
            app.selectbox(key="instrument").select("NSE:TCS").run()
            self.assertFalse(app.exception)
            self.assertEqual(len(app.metric), 0)
            app.selectbox(key="instrument").select("NSE:RELIANCE").run()
            self.assertEqual(app.metric[0].value, "108.00")
            upload.getvalue = lambda: b"not,a,valid,price,file"
            app.form_submit_button(key="load_csv").click().run()
            self.assertFalse(app.exception)
            self.assertEqual(len(app.metric), 0)
            self.assertTrue(any("CSV rejected" in error.value for error in app.error))

    def test_custom_dates_and_single_observation_do_not_crash(self):
        from datetime import date

        app = self.start()
        app.toggle(key="custom_dates").set_value(True).run()
        app.date_input[0].set_value((date(2026, 10, 23), date(2026, 10, 23))).run()
        self.assertFalse(app.exception)
        self.assertTrue(any("only one observation" in c.value for c in app.caption))
        app.date_input[0].set_value((date(2026, 1, 3), date(2026, 1, 4))).run()
        self.assertFalse(app.exception)
        self.assertTrue(any("No observations" in i.value for i in app.info))


if __name__ == "__main__":
    unittest.main()
