import os
import time
import csv
import datetime

if os.name == 'nt':
    import win32gui
else:
    quit('Only Windows is supported at the moment.')

def get_active_window_title_windows():
    hwnd = win32gui.GetForegroundWindow()
    return win32gui.GetWindowText(hwnd)

# Initialize variables
current_app = ""
start_time = datetime.datetime.now()
data_file = "time_tracking_data.csv"

while True:
    # Get the current active window's title
    window_title = get_active_window_title_windows()

    # Check if the application has changed
    if window_title != current_app:
        # Record the previous application's usage time
        end_time = datetime.datetime.now()
        duration = (end_time - start_time).total_seconds()

        # Save the data to the CSV file
        with open(data_file, "a", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([current_app, start_time, end_time, duration])

        # Update the current application and start time
        current_app = window_title
        start_time = datetime.datetime.now()

    # Poll every second
    time.sleep(1)
