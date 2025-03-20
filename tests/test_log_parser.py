import pytest
import datetime
from src.helpers.log_parser import parse_log_line, parse_log_file, filter_logs_by_level, filter_logs_by_time_range

def test_parse_log_line_valid():
    line = "2025-03-18 14:05:10,INFO,Test message"
    result = parse_log_line(line)
    assert result["timestamp"] == datetime.datetime(2025, 3, 18, 14, 5, 10)
    assert result["level"] == "INFO"
    assert result["message"] == "Test message"

def test_parse_log_line_invalid_format():
    line = "invalid log line"
    with pytest.raises(ValueError) as exc_info:
        parse_log_line(line)
    assert "Invalid log line format" in str(exc_info.value)

def test_parse_log_line_invalid_datetime():
    line = "2025-13-45 25:99:99,INFO,Test message"
    with pytest.raises(ValueError) as exc_info:
        parse_log_line(line)
    assert "Invalid date/time format" in str(exc_info.value)

def test_parse_log_file_empty():
    lines = []
    result = parse_log_file(lines)
    assert result == []

def test_parse_log_file_valid():
    lines = [
        "2025-03-18 14:05:10,INFO,Message 1",
        "2025-03-18 14:05:11,ERROR,Message 2",
        "2025-03-18 14:05:12,WARN,Message 3"
    ]
    result = parse_log_file(lines)
    assert len(result) == 3
    assert result[0]["level"] == "INFO"
    assert result[1]["message"] == "Message 2"
    assert result[2]["timestamp"] == datetime.datetime(2025, 3, 18, 14, 5, 12)

def test_parse_log_file_with_empty_lines():
    lines = [
        "",
        "2025-03-18 14:05:10,INFO,Message 1",
        "  ",
        "2025-03-18 14:05:11,ERROR,Message 2",
        ""
    ]
    result = parse_log_file(lines)
    assert len(result) == 2

def test_filter_logs_by_level():
    entries = [
        {"timestamp": datetime.datetime(2025, 3, 18, 14, 5, 10), "level": "INFO", "message": "Info msg"},
        {"timestamp": datetime.datetime(2025, 3, 18, 14, 5, 11), "level": "ERROR", "message": "Error msg"},
        {"timestamp": datetime.datetime(2025, 3, 18, 14, 5, 12), "level": "info", "message": "Another info"}
    ]

    result = filter_logs_by_level(entries, "INFO")
    assert len(result) == 2
    assert all(e["level"].upper() == "INFO" for e in result)

def test_filter_logs_by_level_no_matches():
    entries = [
        {"timestamp": datetime.datetime(2025, 3, 18, 14, 5, 10), "level": "INFO", "message": "Info msg"}
    ]
    result = filter_logs_by_level(entries, "ERROR")
    assert result == []

def test_filter_logs_by_time_range():
    entries = [
        {"timestamp": datetime.datetime(2025, 3, 18, 14, 5, 10), "level": "INFO", "message": "msg1"},
        {"timestamp": datetime.datetime(2025, 3, 18, 14, 5, 11), "level": "ERROR", "message": "msg2"},
        {"timestamp": datetime.datetime(2025, 3, 18, 14, 5, 12), "level": "INFO", "message": "msg3"}
    ]

    start = datetime.datetime(2025, 3, 18, 14, 5, 10)
    end = datetime.datetime(2025, 3, 18, 14, 5, 11)

    result = filter_logs_by_time_range(entries, start, end)
    assert len(result) == 2
    assert all(start <= e["timestamp"] <= end for e in result)

def test_filter_logs_by_time_range_no_matches():
    entries = [
        {"timestamp": datetime.datetime(2025, 3, 18, 14, 5, 10), "level": "INFO", "message": "msg1"}
    ]

    start = datetime.datetime(2025, 3, 18, 14, 5, 11)
    end = datetime.datetime(2025, 3, 18, 14, 5, 12)

    result = filter_logs_by_time_range(entries, start, end)
    assert result == []

def test_filter_logs_by_time_range_inclusive():
    entries = [
        {"timestamp": datetime.datetime(2025, 3, 18, 14, 5, 10), "level": "INFO", "message": "msg1"}
    ]

    start = datetime.datetime(2025, 3, 18, 14, 5, 10)
    end = datetime.datetime(2025, 3, 18, 14, 5, 10)

    result = filter_logs_by_time_range(entries, start, end)
    assert len(result) == 1
