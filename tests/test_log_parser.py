import pytest
from datetime import datetime
from src.helpers.log_parser import parse_log_line, parse_log_file, filter_logs_by_level, filter_logs_by_time_range

def test_parse_log_line_valid():
    line = "2025-03-18 14:05:10,INFO,Test message"
    result = parse_log_line(line)
    assert result["timestamp"] == datetime(2025, 3, 18, 14, 5, 10)
    assert result["level"] == "INFO"
    assert result["message"] == "Test message"

def test_parse_log_line_invalid_format():
    line = "2025-03-18 14:05:10,INFO"
    with pytest.raises(ValueError) as exc:
        parse_log_line(line)
    assert "Invalid log line format" in str(exc.value)

def test_parse_log_line_invalid_datetime():
    line = "invalid-date,INFO,Test message"
    with pytest.raises(ValueError) as exc:
        parse_log_line(line)
    assert "Invalid date/time format" in str(exc.value)

def test_parse_log_file_empty():
    lines = []
    result = parse_log_file(lines)
    assert result == []

def test_parse_log_file_valid():
    lines = [
        "2025-03-18 14:05:10,INFO,Message 1",
        "2025-03-18 14:05:11,ERROR,Message 2",
        ""  # Empty line should be ignored
    ]
    result = parse_log_file(lines)
    assert len(result) == 2
    assert result[0]["message"] == "Message 1"
    assert result[1]["level"] == "ERROR"

def test_filter_logs_by_level():
    entries = [
        {"timestamp": datetime.now(), "level": "INFO", "message": "Info msg"},
        {"timestamp": datetime.now(), "level": "ERROR", "message": "Error msg"},
        {"timestamp": datetime.now(), "level": "info", "message": "Info msg 2"}
    ]

    result = filter_logs_by_level(entries, "INFO")
    assert len(result) == 2
    assert all(e["level"].upper() == "INFO" for e in result)

def test_filter_logs_by_time_range():
    t1 = datetime(2025, 3, 18, 14, 0)
    t2 = datetime(2025, 3, 18, 14, 30)
    t3 = datetime(2025, 3, 18, 15, 0)

    entries = [
        {"timestamp": t1, "level": "INFO", "message": "First"},
        {"timestamp": t2, "level": "INFO", "message": "Second"},
        {"timestamp": t3, "level": "INFO", "message": "Third"}
    ]

    result = filter_logs_by_time_range(entries, t1, t2)
    assert len(result) == 2
    assert result[0]["message"] == "First"
    assert result[1]["message"] == "Second"

def test_filter_logs_by_time_range_empty():
    t1 = datetime(2025, 3, 18, 14, 0)
    t2 = datetime(2025, 3, 18, 14, 30)

    entries = [
        {"timestamp": datetime(2025, 3, 18, 13, 0), "level": "INFO", "message": "Too early"},
        {"timestamp": datetime(2025, 3, 18, 15, 0), "level": "INFO", "message": "Too late"}
    ]

    result = filter_logs_by_time_range(entries, t1, t2)
    assert result == []

def test_parse_log_line_with_commas():
    line = "2025-03-18 14:05:10,INFO,Message with, multiple, commas"
    result = parse_log_line(line)
    assert result["message"] == "Message with, multiple, commas"

def test_parse_log_line_whitespace():
    line = "2025-03-18 14:05:10,INFO,Test message"  # No extra whitespace
    result = parse_log_line(line)
    assert result["timestamp"] == datetime(2025, 3, 18, 14, 5, 10)
    assert result["level"] == "INFO"
    assert result["message"] == "Test message"
