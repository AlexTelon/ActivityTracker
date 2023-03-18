import csv
import re
import time
import win32gui
import json

def match_pattern(class_name, title, pattern_class, pattern_title):
    if not pattern_class and not pattern_title:
        return False
    if pattern_class and not re.search(pattern_class, class_name):
        return False
    if pattern_title and not re.search(pattern_title, title):
        return False
    return True

def find_window_name(class_name, title):
    for win_pattern in patterns:
        pattern_class = win_pattern.get("class")
        pattern_title = win_pattern.get("title")
        if match_pattern(class_name, title, pattern_class, pattern_title):
            return win_pattern["name"]
    return None

# Load patterns from the JSON file
with open('patterns.json', 'r') as file:
    patterns = json.load(file)

with open('time_tracking_data.csv', 'w', newline='') as csvfile:
    fieldnames = ['timestamp', 'window_name']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    while True:
        # Get the active window
        hwnd = win32gui.GetForegroundWindow()

        # Check if the window is visible
        if not win32gui.IsWindowVisible(hwnd):
            print("Window is not visible")
        else:
            # Get the class name and title of the window
            class_name = win32gui.GetClassName(hwnd)
            title = win32gui.GetWindowText(hwnd)
            
            # Find the window name based on the class name and title
            window_name = find_window_name(class_name, title)
            
            # Write the window name and current timestamp to the CSV file
            timestamp = int(time.time())
            writer.writerow({'timestamp': timestamp, 'window_name': window_name or f'other {title=} {class_name=}'})
            csvfile.flush()

        # Poll every x seconds
        time.sleep(1)
