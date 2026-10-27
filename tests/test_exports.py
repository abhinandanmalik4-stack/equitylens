from dataclasses import replace
import unittest

from equitylens.catalog import INSTRUMENTS
from equitylens.csv_data import import_history
from equitylens.exports import dataset_id, export_history
from equitylens.providers import DemoProvider


class ExportTests(unittest.TestCase):
    def setUp(self):
        self.history = DemoProvider().history(INSTRUMENTS[0])

    def test_roundtrip_keeps_demo_marker_and_values(self):
        raw = export_history(self.history, self.history.frame.tail(5))
        imported = import_history(raw, INSTRUMENTS[0], "Reimported demo", "Synthetic", is_demo=False)
        self.assertTrue(imported.is_demo)
        self.assertEqual(imported.frame.close.tolist(), self.history.frame.close.tail(5).tolist())
        self.assertIn(b"adjustment", raw)

    def test_identifier_changes_when_data_or_provenance_changes(self):
        self.assertEqual(dataset_id(self.history), dataset_id(DemoProvider().history(INSTRUMENTS[0])))
        self.assertNotEqual(dataset_id(self.history), dataset_id(replace(self.history, source="Another source")))

    def test_export_cannot_misattribute_altered_rows(self):
        altered = self.history.frame.tail(1).copy()
        altered["volume"] = 1
        with self.assertRaises(ValueError):
            export_history(self.history, altered)

    def test_metadata_is_not_a_spreadsheet_formula(self):
        changed = replace(self.history, adjustment="=1+1")
        self.assertIn(b"'=1+1", export_history(changed))


if __name__ == "__main__":
    unittest.main()
