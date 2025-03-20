def kmp_search(text: str, pattern: str) -> list[int]:
    """
    Knuth-Morris-Pratt string matching.
    Returns the list of starting indices where 'pattern' is found in 'text'.
    """
    if not pattern:
        return []
    lps = _compute_lps_array(pattern)
    matches = []

    i = 0  # index for text
    j = 0  # index for pattern
    while i < len(text):
        if text[i] == pattern[j]:
            i += 1
            j += 1
            if j == len(pattern):
                matches.append(i - j)
                j = lps[j - 1]
        else:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return matches


def _compute_lps_array(pattern: str) -> list[int]:
    """
    Compute the "longest prefix which is also a suffix" array (LPS),
    used by the KMP algorithm to skip unnecessary comparisons.
    """
    lps = [0] * len(pattern)
    prev_lps = 0  # length of the previous longest prefix suffix
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[prev_lps]:
            prev_lps += 1
            lps[i] = prev_lps
            i += 1
        else:
            if prev_lps != 0:
                prev_lps = lps[prev_lps - 1]
            else:
                lps[i] = 0
                i += 1
    return lps
