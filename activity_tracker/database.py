import sqlite3
import time
import datetime

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.init_db()

    def init_db(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS window_data
                                (timestamp INTEGER, window_name TEXT)''')
        self.conn.commit()

    def add_row(self, window_name):
        timestamp = int(time.time())
        print(f"writing '{window_name}' to db")
        self.cursor.execute("INSERT INTO window_data (timestamp, window_name) VALUES (?, ?)", (timestamp, window_name))
        self.conn.commit()

    def close(self):
        self.conn.close()


def read_all():
    with sqlite3.connect('time_tracking_data.sqlite') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT timestamp, window_name FROM window_data")
        data = cursor.fetchall()
    return data


def read_data_from_date(date):
    filtered_data = []
    for timestamp, window_name in read_all():
        dt = datetime.datetime.fromtimestamp(timestamp)
        if date == dt.date():
            filtered_data.append((dt, window_name))
    return filtered_data