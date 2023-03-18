import re
import win32gui
import patterns

def enum_windows(hwnd, results):
    if win32gui.IsWindowVisible(hwnd):
        class_name = win32gui.GetClassName(hwnd)
        title = win32gui.GetWindowText(hwnd)
        results.append((hwnd, class_name, title))

windows = []
win32gui.EnumWindows(enum_windows, windows)

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

stuff = set()
for hwnd, class_name, title in windows:
    for win_name, win_pattern in patterns.patterns.items():
        pattern_class = win_pattern.get("class")
        pattern_title = win_pattern.get("title")
        name = find_window_name(class_name, title)
        if name:
            ...
            # print(name)
        else:
            stuff.add(f'{title=}, {class_name=}')

for x in stuff:
    print(x)