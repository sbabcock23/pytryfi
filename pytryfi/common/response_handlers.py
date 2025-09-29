import datetime

def parse_fi_date(input: str) -> datetime.datetime:
    return datetime.datetime.fromisoformat(input.replace('Z', '+00:00'))