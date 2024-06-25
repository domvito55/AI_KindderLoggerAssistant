from datetime import datetime

def extract_date_time_from_filename(filename):
    parts = filename.split(" at ")
    date_part = parts[0].split(" ")[-1]
    time_part = parts[1].split("_")[0].replace(".", ":")
    datetime_str = f"{date_part} {time_part}"
    return datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")