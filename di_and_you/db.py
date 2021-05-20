import os
import sqlite3
from typing import List, Optional

from .csv_loader import Row, load_csv_v1

DB_PATH = "factors.db"

_create_table = """
CREATE TABLE IF NOT EXISTS factors (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT NOT NULL,
    spectral_range  TEXT NOT NULL,
    bands           TEXT NOT NULL,
    cba_factor      REAL NOT NULL
)
"""

_insert_row = """
INSERT INTO factors (name, spectral_range, bands, cba_factor)
VALUES (?, ?, ?, ?)
"""

_find_row = """
SELECT
    name
    , spectral_range
    , bands
    , cba_factor
FROM factors
WHERE
    name = ?
"""

conn = sqlite3.connect(DB_PATH)


def make_connection(path: str):
    return sqlite3.connect(path)


class FactorDbV1:
    def load_db(self):
        # TODO this is io, inject conn
        cur = conn.cursor()
        cur.execute(_create_table)
        conn.commit()
        data = load_csv_v1()
        for row in data:
            conn.execute(_insert_row, row)
        conn.commit()

    def find(self, product_name: str) -> Row:
        # TODO inject this again!
        cur = conn.cursor()
        cur.execute(_find_row, (product_name,))
        return Row(*cur.fetchone())

    def count(self) -> int:
        # TODO inject this again!
        cur = conn.cursor()
        cur.execute("SELECT count(*) FROM factors;")
        cnt = cur.fetchone()[0]
        return cnt

    def cleanup(self):
        conn.close()
        # TODO more io, but shoule we should inject this?
        os.remove(DB_PATH)


class FactorDbV2:
    def __init__(self, conn: sqlite3.Connection, path: Optional[str] = None):
        # we're relying on IoC here, we don't construct the dependency
        # because we might want to replace it's implementation at runtime.
        self._conn = conn
        self._path = path

    def load_db(self, data: List[Row]):
        # we injected the connection into the class initializer
        cur = self._conn.cursor()
        cur.execute(_create_table)
        self._conn.commit()
        for row in data:
            cur.execute(_insert_row, row)
        self._conn.commit()

    def find(self, product_name: str) -> Row:
        cur = self._conn.cursor()
        cur.execute(_find_row, (product_name,))
        return Row(*cur.fetchone())

    def count(self) -> int:
        cur = self._conn.cursor()
        cur.execute("SELECT count(*) FROM factors;")
        cnt = cur.fetchone()[0]
        return cnt

    def cleanup(self):
        self._conn.close()

        if self._path is not None:
            # this represents a weird sticky point in dependency injection
            # should I do something like create a "Finalizer" to abstract this?
            # that seems like overkill, but _might_ be useful sometimes
            os.remove(self._path)
