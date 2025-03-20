import pytest
from src.helpers.dsl_parser import parse_dsl


def test_parse_dsl_set_command():
    dsl = "SET x = 42"
    result = parse_dsl(dsl)
    assert result == [{"type": "SET", "var": "x", "value": 42}]


def test_parse_dsl_incr_command():
    dsl = "INCR counter BY 5"
    result = parse_dsl(dsl)
    assert result == [{"type": "INCR", "var": "counter", "amount": 5}]


def test_parse_dsl_if_command():
    dsl = "IF score > 100 THEN SET level = 2"
    result = parse_dsl(dsl)
    assert result == [{
        "type": "IF",
        "var": "score",
        "op": ">",
        "value": 100,
        "then": "SET level = 2"
    }]


def test_parse_dsl_multiple_commands():
    dsl = """
    SET x = 1
    INCR x BY 5
    IF x > 5 THEN SET y = 10
    """
    result = parse_dsl(dsl)
    assert result == [
        {"type": "SET", "var": "x", "value": 1},
        {"type": "INCR", "var": "x", "amount": 5},
        {
            "type": "IF",
            "var": "x",
            "op": ">",
            "value": 5,
            "then": "SET y = 10"
        }
    ]


def test_parse_dsl_empty_lines():
    dsl = """

    SET x = 1

    INCR x BY 5

    """
    result = parse_dsl(dsl)
    assert result == [
        {"type": "SET", "var": "x", "value": 1},
        {"type": "INCR", "var": "x", "amount": 5}
    ]


def test_parse_dsl_case_insensitive():
    dsl = """
    set x = 1
    incr x by 5
    if x > 5 then SET y = 10
    """
    result = parse_dsl(dsl)
    assert result == [
        {"type": "SET", "var": "x", "value": 1},
        {"type": "INCR", "var": "x", "amount": 5},
        {
            "type": "IF",
            "var": "x",
            "op": ">",
            "value": 5,
            "then": "SET y = 10"
        }
    ]


def test_parse_dsl_whitespace_variations():
    dsl = """
    SET    x=1
    INCR   x   BY    5
    IF x>5    THEN SET y = 10
    """
    result = parse_dsl(dsl)
    assert result == [
        {"type": "SET", "var": "x", "value": 1},
        {"type": "INCR", "var": "x", "amount": 5},
        {
            "type": "IF",
            "var": "x",
            "op": ">",
            "value": 5,
            "then": "SET y = 10"
        }
    ]


def test_parse_dsl_invalid_command():
    with pytest.raises(ValueError) as exc_info:
        parse_dsl("INVALID x = 1")
    assert str(exc_info.value) == "Invalid DSL line: 'INVALID x = 1'"


def test_parse_dsl_invalid_set_format():
    with pytest.raises(ValueError) as exc_info:
        parse_dsl("SET x = abc")
    assert str(exc_info.value) == "Invalid DSL line: 'SET x = abc'"


def test_parse_dsl_invalid_incr_format():
    with pytest.raises(ValueError) as exc_info:
        parse_dsl("INCR x BY abc")
    assert str(exc_info.value) == "Invalid DSL line: 'INCR x BY abc'"


def test_parse_dsl_invalid_if_format():
    with pytest.raises(ValueError) as exc_info:
        parse_dsl("IF x > abc THEN SET y = 1")
    assert str(exc_info.value) == "Invalid DSL line: 'IF x > abc THEN SET y = 1'"
