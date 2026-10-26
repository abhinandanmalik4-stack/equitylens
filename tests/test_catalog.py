import unittest

from equitylens.catalog import INSTRUMENTS, Instrument, get_instrument, search_instruments


class CatalogTests(unittest.TestCase):
    def test_search_name_sector_and_case(self):
        self.assertEqual(search_instruments("  infosys ")[0].symbol, "INFY")
        self.assertEqual(len(search_instruments("BANKING")), 2)
        self.assertEqual(search_instruments("no such company"), ())

    def test_unknown_identity_is_rejected(self):
        with self.assertRaises(ValueError):
            get_instrument("NASDAQ:TCS")

    def test_exchange_is_part_of_identity(self):
        self.assertEqual(len({i.key for i in INSTRUMENTS}), len(INSTRUMENTS))
        future = Instrument("AAPL", "Apple", "Technology", "NASDAQ", "USD", "US")
        self.assertEqual(future.key, "NASDAQ:AAPL")


if __name__ == "__main__":
    unittest.main()
