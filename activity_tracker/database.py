from collections import defaultdict
import sqlite3
import time
from datetime import datetime, time as dt_time
from typing import Tuple

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
        dt = datetime.fromtimestamp(timestamp)
        if date == dt.date():
            filtered_data.append((dt, window_name))
    return filtered_data

def read_data_from_dates(begin: datetime, end: datetime) -> dict[datetime, list[Tuple[datetime, str]]]:
    """Returns a dictionary where the keys are dates with data and a list of the data from that day.
    Dates are inclusive.
    """
    # TODO fix ugly import dt_time and datetime and time overall.
    begin = datetime.combine(begin, dt_time.min)
    end = datetime.combine(end, dt_time.max)
    result = defaultdict(list)
    for timestamp, window_name in read_all():
        dt = datetime.fromtimestamp(timestamp)
        if begin <= dt <= end:
            result[dt.date()].append((dt, window_name))
    return result

def print_database_contents():
    with sqlite3.connect('time_tracking_data.sqlite') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM window_data")
        data = cursor.fetchall()
        for row in data:
            print(row)


if __name__ == "__main__":
    print_database_contents()