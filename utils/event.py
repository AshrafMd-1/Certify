from datetime import datetime


def max_allowed_offset_year(selected_year, offset):
    current_year = datetime.now().year
    if abs(current_year - selected_year) > offset:
        return False
    return True


def convert_24_to_12(time):
    if time == "00:00:00":
        return "12:00 AM"
    if time == "12:00:00":
        return "12:00 PM"
    time = time.split(":")
    hour = int(time[0])
    minute = time[1]
    if hour < 12:
        return f"{hour}:{minute} AM"
    return f"{hour - 12}:{minute} PM"
