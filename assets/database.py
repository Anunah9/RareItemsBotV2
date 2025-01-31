import sqlite3
import time


class SqliteItemsRepository:
    def __init__(self, db_path):
        self.db = sqlite3.Connection(db_path)

    def get_track_items(self):
        cur = self.db.cursor()
        items = cur.execute("SELECT * FROM TrackItems").fetchall()

        return [{item[0]: item[1]} for item in items]


class Items:
    def __init__(self, repository: SqliteItemsRepository):
        self.repository: SqliteItemsRepository = repository

    def get_track_items(self):
        return self.repository.get_track_items()
