from datetime import datetime

def parse_date(date_str: str, fmt: str = "%d-%b-%y") -> datetime:
    """
    Parses a date string in the format used in CSVs like "1-Jan-25"
    to a datetime object.
    """
    return datetime.strptime(date_str.strip(), fmt)
