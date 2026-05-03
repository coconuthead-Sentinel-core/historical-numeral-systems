"""
Arabic Abjad — letter values + chronograms.

Abjad order (the original 28-letter alphabetic ordering before modern alphabetical):
    ا=1   ب=2   ج=3   د=4   ه=5   و=6   ز=7   ح=8   ط=9
    ي=10  ك=20  ل=30  م=40  ن=50  س=60  ع=70  ف=80  ص=90
    ق=100 ر=200 ش=300 ت=400 ث=500 خ=600 ذ=700 ض=800 ظ=900 غ=1000

Chronograms: encode a date by selecting words whose abjad sum equals the year.
Used historically in Islamic chronograms, talismans, and named dates.
"""
from __future__ import annotations
from ..primitives import digital_root


ABJAD_VALUES = {
    "ا": 1,    "أ": 1,    "إ": 1,    "آ": 1,
    "ب": 2,    "ج": 3,    "د": 4,    "ه": 5,    "ة": 5,
    "و": 6,    "ز": 7,    "ح": 8,    "ط": 9,
    "ي": 10,   "ى": 10,   "ك": 20,   "ل": 30,   "م": 40,
    "ن": 50,   "س": 60,   "ع": 70,   "ف": 80,   "ص": 90,
    "ق": 100,  "ر": 200,  "ش": 300,  "ت": 400,  "ث": 500,
    "خ": 600,  "ذ": 700,  "ض": 800,  "ظ": 900,  "غ": 1000,
    # Latin transliteration approximations
}

# Latin transliteration mapping (Arabic phonetic to abjad)
LATIN_TO_ABJAD = {
    "a": 1,    "b": 2,    "j": 3,    "d": 4,    "h": 5,
    "w": 6,    "z": 7,    "y": 10,   "k": 20,   "l": 30,
    "m": 40,   "n": 50,   "s": 60,   "f": 80,   "q": 100,
    "r": 200,  "t": 400,  "g": 1000,
}


def value(char: str) -> int:
    """Abjad value of a single character (0 if unknown)."""
    if char in ABJAD_VALUES:
        return ABJAD_VALUES[char]
    c = char.lower()
    return LATIN_TO_ABJAD.get(c, 0)


def sum_word(text: str) -> int:
    """Sum the abjad values of all characters."""
    return sum(value(c) for c in text)


def reduce(text: str) -> int:
    return digital_root(sum_word(text))


def chronogram(text: str, target_year: int) -> dict:
    """
    Test whether a word/phrase is a valid chronogram for a given year.
    Returns whether the abjad sum matches + the actual sum + delta.
    """
    s = sum_word(text)
    return {
        "text":     text,
        "sum":      s,
        "target":   target_year,
        "matches":  s == target_year,
        "delta":    s - target_year,
    }


def fingerprint(text: str) -> dict:
    s = sum_word(text)
    return {
        "text":         text,
        "abjad_sum":    s,
        "digital_root": digital_root(s),
        "char_count":   sum(1 for c in text if value(c) > 0),
    }
