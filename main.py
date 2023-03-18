import time
import csv
import datetime
import re
import win32gui
import configparser

def get_active_window_title_windows(patterns):
    hwnd = win32gui.GetForegroundWindow()
    window_title = win32gui.GetWindowText(hwnd)
    title = ' '.join(window_title.strip().split())
    print(title)
    # Match window title against predefined patterns
    for app, pattern in patterns.items():
        if re.match(pattern, title):
            return app

    # If no match is found, return 'Other'
    return "Other"

# Read patterns from a config file
config = configparser.ConfigParser()
config.read("patterns.ini")
patterns = dict(config["patterns"])

# Initialize variables
current_app = ""
data_file = "time_tracking_data.csv"

while True:
    # Get the current active window's title
    window_title = get_active_window_title_windows(patterns)
    print(window_title)
    # Check if the application has changed
    if window_title != current_app:
        # Record the timestamp and application
        timestamp = datetime.datetime.now()

        # # Save the data to the CSV file
        # with open(data_file, "a", newline='', encoding='utf-8') as f:
        #     writer = csv.writer(f)
        #     writer.writerow([current_app, timestamp])

        # Update the current application
        current_app = window_title

    # Poll every x seconds
    time.sleep(1)
