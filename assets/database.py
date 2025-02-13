import sqlite3
import time


class SqliteItemsRepository:
    def __init__(self, db_path):
        self.db = sqlite3.Connection(db_path)

    def get_track_items(self):
        cur = self.db.cursor()
        items = cur.execute("SELECT * FROM TrackItems").fetchall()

        return [{item[0]: item[1]} for item in items]

    def add_to_checked(self, listing_id):
        self.db.cursor().execute(f"INSERT INTO Checked VALUES ({listing_id})")
        self.db.commit()

    def check(self, listing_id) -> bool:
        if self.db.cursor().execute(f"SELECT * FROM Checked WHERE listingid={listing_id}").fetchone():
            return True
        return False

    def add_to_bought_items(self, item_name, listing_id, price, stickers_price, date):
        self.db.cursor().execute(
            f"INSERT INTO BoughtItems VALUES (\"{item_name}\", {listing_id}, {price}, {stickers_price}, \"{date}\")")
        self.db.commit()


class Items:
    def __init__(self, repository: SqliteItemsRepository):
        self.repository: SqliteItemsRepository = repository

    def get_track_items(self):
        return self.repository.get_track_items()

    def add_to_checked(self, listing_id):
        self.repository.add_to_checked(listing_id)

    def check(self, listing_id) -> bool:
        return self.repository.check(listing_id)

    def add_to_bought_items(self, item_name, listing_id, price,  stickers_price, date):
        return self.repository.add_to_bought_items(item_name, listing_id, price, stickers_price, date)
