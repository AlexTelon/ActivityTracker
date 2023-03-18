import re
import time
import win32gui
import patterns

def match_pattern(class_name, title, pattern_class, pattern_title):
    if not pattern_class and not pattern_title:
        return False
    if pattern_class and not re.search(pattern_class, class_name):
        return False
    if pattern_title and not re.search(pattern_title, title):
        return False
    return True

def find_window_name(class_name, title):
    for win_name, win_pattern in patterns.patterns.items():
        pattern_class = win_pattern.get("class")
        pattern_title = win_pattern.get("title")
        if match_pattern(class_name, title, pattern_class, pattern_title):
            return win_name
    return None

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
        
        # Print the window name, or "other" if no matching pattern is found
        if window_name:
            print(f"Active Window: {window_name}")
        else:
            print(f"Active Window: other ({title=}, {class_name=})")

    # Poll every x seconds
    time.sleep(1)