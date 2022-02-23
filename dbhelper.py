import sqlite3
import logging
import threading

lock = threading.Lock()


class DBHelper:
    def __init__(self, dbname="data.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    def setup(self):
        stmt = ('''
        CREATE TABLE IF NOT EXISTS config
        (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        symbol INTEGER default 0,
        alert_enabled  INTEGER  default 1 NOT NULL
        );
        ''')
        try:
            self.conn.executescript(stmt)
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error(str(e))
