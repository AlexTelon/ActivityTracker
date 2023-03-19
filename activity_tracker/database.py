import sqlite3

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.init_db()

    def init_db(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS window_data
                                (timestamp INTEGER, window_name TEXT)''')
        self.conn.commit()

    def add_row(self, timestamp, window_name):
        print(f"writing '{window_name}' to db")
        self.cursor.execute("INSERT INTO window_data (timestamp, window_name) VALUES (?, ?)", (timestamp, window_name))
        self.conn.commit()

    def close(self):
        self.conn.close()
