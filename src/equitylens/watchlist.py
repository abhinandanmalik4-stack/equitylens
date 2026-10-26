"""Local, single-user watchlist persistence. Not an authenticated portfolio."""

import sqlite3
from contextlib import closing, contextmanager
from pathlib import Path

from equitylens.catalog import get_instrument


class Watchlist:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as connection:
            connection.execute("CREATE TABLE IF NOT EXISTS watchlist (instrument TEXT PRIMARY KEY)")

    @contextmanager
    def _connect(self):
        # sqlite's transaction context commits/rolls back, but does not close.
        with closing(sqlite3.connect(self.path, timeout=5)) as connection:
            with connection:
                yield connection

    def items(self) -> list[str]:
        with self._connect() as connection:
            return [row[0] for row in connection.execute("SELECT instrument FROM watchlist ORDER BY instrument")]

    def add(self, key: str) -> None:
        get_instrument(key)
        with self._connect() as connection:
            connection.execute("INSERT OR IGNORE INTO watchlist (instrument) VALUES (?)", (key,))

    def remove(self, key: str) -> None:
        with self._connect() as connection:
            connection.execute("DELETE FROM watchlist WHERE instrument = ?", (key,))
