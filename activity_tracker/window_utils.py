import re

def match_pattern(class_name, title, pattern_class, pattern_title):
    """
    Check if the given class_name and title match the pattern_class and pattern_title.
    
    :param class_name: The class name of the window.
    :param title: The title of the window.
    :param pattern_class: The class pattern to match against.
    :param pattern_title: The title pattern to match against.
    :return: True if both patterns match, False otherwise.
    """
    if not pattern_class and not pattern_title:
        return False
    if pattern_class and not re.search(pattern_class, class_name):
        return False
    if pattern_title and not re.search(pattern_title, title):
        return False
    return True

def find_window_name(class_name, title, patterns):
    """
    Find the window name based on the class name and title using the given patterns.
    
    :param class_name: The class name of the window.
    :param title: The title of the window.
    :param patterns: The list of window patterns to match against.
    :return: The window name if a match is found, None otherwise.
    """
    for win_pattern in patterns:
        pattern_class = win_pattern.get("class")
        pattern_title = win_pattern.get("title")
        if match_pattern(class_name, title, pattern_class, pattern_title):
            return win_pattern["name"]
    return None
