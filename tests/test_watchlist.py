from pathlib import Path
import tempfile
import unittest

from equitylens.watchlist import Watchlist


class WatchlistTests(unittest.TestCase):
    def test_persistence_deduplication_and_removal(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "nested" / "watchlist.db"
            first = Watchlist(path)
            first.add("NSE:INFY")
            first.add("NSE:INFY")
            second = Watchlist(path)
            self.assertEqual(second.items(), ["NSE:INFY"])
            second.remove("NSE:INFY")
            second.remove("NSE:INFY")
            self.assertEqual(first.items(), [])

    def test_unknown_or_injection_key_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            store = Watchlist(Path(directory) / "watchlist.db")
            with self.assertRaises(ValueError):
                store.add("NSE:INFY'); DROP TABLE watchlist; --")
            self.assertEqual(store.items(), [])


if __name__ == "__main__":
    unittest.main()
