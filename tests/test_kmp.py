import pytest
from src.algorithms.kmp import kmp_search

def test_kmp_basic_match():
    text = "ABABDABACDABABCABAB"
    pattern = "ABABCABAB"
    assert kmp_search(text, pattern) == [10]

def test_kmp_multiple_matches():
    text = "AABAACAADAABAABA"
    pattern = "AABA"
    assert kmp_search(text, pattern) == [0, 9, 12]

def test_kmp_no_match():
    text = "ABABDABACDABABCABAB"
    pattern = "XYZ"
    assert kmp_search(text, pattern) == []

def test_kmp_empty_pattern():
    text = "ABCDEF"
    pattern = ""
    assert kmp_search(text, pattern) == []

def test_kmp_empty_text():
    text = ""
    pattern = "ABC"
    assert kmp_search(text, pattern) == []

def test_kmp_pattern_longer_than_text():
    text = "ABC"
    pattern = "ABCDEF"
    assert kmp_search(text, pattern) == []

def test_kmp_single_char_pattern():
    text = "AAAA"
    pattern = "A"
    assert kmp_search(text, pattern) == [0, 1, 2, 3]

def test_kmp_overlapping_matches():
    text = "AAAAA"
    pattern = "AA"
    assert kmp_search(text, pattern) == [0, 1, 2, 3]

def test_kmp_pattern_equals_text():
    text = "ABCDEF"
    pattern = "ABCDEF"
    assert kmp_search(text, pattern) == [0]

def test_kmp_special_chars():
    text = "!@#$%^&*()"
    pattern = "#$%"
    assert kmp_search(text, pattern) == [2]
