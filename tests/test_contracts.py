from dataclasses import replace
import unittest

from equitylens.catalog import INSTRUMENTS, Instrument
from equitylens.providers import DemoProvider, validate_history


class ContractTests(unittest.TestCase):
    def test_bad_instrument_identity_is_rejected_before_storage(self):
        for fields in ({"symbol": "TCS:NSE"}, {"exchange": " NSE"}, {"name": ""},
                       {"currency": "inr"}, {"country": "IND"}, {"symbol": "TCS\n"}, {"name": None}):
            with self.subTest(fields=fields):
                with self.assertRaises(ValueError):
                    replace(INSTRUMENTS[0], **fields)
        self.assertEqual(Instrument("BRK.B", "Example", "Finance", "NYSE", "USD", "US").key, "NYSE:BRK.B")

    def test_missing_or_mistyped_history_metadata_has_controlled_errors(self):
        original = DemoProvider().history(INSTRUMENTS[0])
        for fields in ({"source": None}, {"adjustment": 123}, {"instrument": "NSE:RELIANCE"},
                       {"is_demo": "False"}, {"frame": None}):
            with self.subTest(fields=fields):
                with self.assertRaises(ValueError):
                    replace(original, **fields)
        with self.assertRaises(ValueError):
            validate_history([])


if __name__ == "__main__":
    unittest.main()
