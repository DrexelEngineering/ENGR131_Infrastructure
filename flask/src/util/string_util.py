import re

def is_string_number_combo(s):
    pattern = r'^[A-Za-z]+_[0-9]+$'
    return bool(re.match(pattern, s))

def extract_string_number(s):
    pattern = r'^([A-Za-z]+)_([0-9]+)$'
    match = re.match(pattern, s)
    if match:
        return match.group(1), int(match.group(2))