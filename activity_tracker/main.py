import argparse
import time
import win32gui
import json
import signal
import win32api

from .window_utils import find_window_name
from .database import Database

IDLE_THRESHOLD = 60  # Time in seconds

def get_idle_time():
    last_input = win32api.GetLastInputInfo()
    current_time = win32api.GetTickCount()
    return (current_time - last_input) / 1000  # Convert milliseconds to seconds

def exit_handler(signal, frame):
    db.add_row("offline")
    db.close()
    exit(0)

signal.signal(signal.SIGINT, exit_handler)
signal.signal(signal.SIGTERM, exit_handler)

parser = argparse.ArgumentParser()
parser.add_argument('db', help='Path to the sqlite database', default='time_tracking_data.sqlite')
args = parser.parse_args()

with open('patterns.json', 'r') as file:
    patterns = json.load(file)

db = Database(args.db)
db.add_row("offline")

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
    db.add_row(window_name or 'other')

    time.sleep(10)
