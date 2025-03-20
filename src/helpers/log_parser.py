import datetime


def parse_log_line(line: str):
    """
    Parse a single log line in the format:
        YYYY-MM-DD HH:MM:SS,LEVEL,Message
    Returns a dict with keys: 'timestamp', 'level', 'message'.
    Raises ValueError if the line is invalid.
    """
    parts = line.split(",", 2)
    if len(parts) < 3:
        raise ValueError(f"Invalid log line format: {line}")

    datetime_part, level, message = parts
    try:
        # Example: 2025-03-18 14:05:10
        timestamp = datetime.datetime.strptime(datetime_part, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        raise ValueError(f"Invalid date/time format: {datetime_part}")

    return {
        "timestamp": timestamp,
        "level": level.strip(),
        "message": message.strip()
    }


def parse_log_file(lines: list[str]) -> list[dict]:
    """
    Parse multiple lines of logs and return a list of structured log entries.
    """
    entries = []
    for line in lines:
        line = line.strip()
        if line:
            entry = parse_log_line(line)
            entries.append(entry)
    return entries


def filter_logs_by_level(entries: list[dict], level: str) -> list[dict]:
    """
    Filter log entries by the given level (e.g., 'ERROR' or 'INFO').
    Level matching is case-insensitive.
    """
    level_upper = level.upper()
    return [e for e in entries if e["level"].upper() == level_upper]


def filter_logs_by_time_range(entries: list[dict], start: datetime.datetime, end: datetime.datetime) -> list[dict]:
    """
    Filter log entries whose timestamp is between start and end (inclusive).
    """
    return [e for e in entries if start <= e["timestamp"] <= end]
