import time
import win32gui
import json
import sqlite3
import signal
from window_utils import find_window_name

def exit_handler(signal, frame):
    # Removes the KeyboardInterupt exception text from the console for instance.
    exit(0)

# Catch signals (Ctrl-C and others)
signal.signal(signal.SIGINT, exit_handler)
signal.signal(signal.SIGTERM, exit_handler)

with open('patterns.json', 'r') as file:
    patterns = json.load(file)

with sqlite3.connect('time_tracking_data.sqlite') as conn:
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS window_data
                      (timestamp INTEGER, window_name TEXT)''')

    while True:
        hwnd = win32gui.GetForegroundWindow()

        if win32gui.IsWindowVisible(hwnd):
            class_name = win32gui.GetClassName(hwnd)
            title = win32gui.GetWindowText(hwnd)

            window_name = find_window_name(class_name, title, patterns)
            if not window_name:
                print('No match for window: %s - %s' % (class_name, title))

            timestamp = int(time.time())
            cursor.execute("INSERT INTO window_data (timestamp, window_name) VALUES (?, ?)", (timestamp, window_name or 'other'))
            conn.commit()

        time.sleep(10)
