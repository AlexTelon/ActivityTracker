import time
import win32gui
import json
import sqlite3
import signal
from window_utils import find_window_name
import win32api

IDLE_THRESHOLD = 60  # Time in seconds

def get_idle_time():
    last_input = win32api.GetLastInputInfo()
    current_time = win32api.GetTickCount()
    return (current_time - last_input) / 1000  # Convert milliseconds to seconds

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
        idle_time = get_idle_time()
        if idle_time > IDLE_THRESHOLD:
            window_name = "idle"
        else:
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

        print(f"[{timestamp}] {window_name}")

        time.sleep(10)
