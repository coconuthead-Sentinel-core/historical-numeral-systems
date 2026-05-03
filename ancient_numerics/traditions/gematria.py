"""
Hebrew Gematria — letter→integer mapping with sum + reduction operations.

The standard mispar hechrachi (absolute value) Hebrew alphabet:
    א=1  ב=2  ג=3  ד=4  ה=5  ו=6  ז=7  ח=8  ט=9
    י=10 כ=20 ל=30 מ=40 נ=50 ס=60 ע=70 פ=80 צ=90
    ק=100 ר=200 ש=300 ת=400

Modern adaptation: also accepts Latin transliteration via standard
Hebrew→Latin mapping (a=א=1, b=ב=2, g=ג=3, etc).
"""
from __future__ import annotations
from ..primitives import digital_root


HEBREW_VALUES = {
    "א": 1,   "ב": 2,   "ג": 3,   "ד": 4,   "ה": 5,
    "ו": 6,   "ז": 7,   "ח": 8,   "ט": 9,
    "י": 10,  "כ": 20,  "ל": 30,  "מ": 40,  "נ": 50,
    "ס": 60,  "ע": 70,  "פ": 80,  "צ": 90,
    "ק": 100, "ר": 200, "ש": 300, "ת": 400,
    # Final forms (sofit) — usually equal their non-final form
    "ך": 20,  "ם": 40,  "ן": 50,  "ף": 80,  "ץ": 90,
}

# Latin transliteration approximation (Sephardic style)
LATIN_TO_HEBREW = {
    "a": "א", "b": "ב", "g": "ג", "d": "ד", "h": "ה",
    "v": "ו", "w": "ו", "z": "ז", "j": "ח", "y": "י",
    "k": "כ", "l": "ל", "m": "מ", "n": "נ", "s": "ס",
    "p": "פ", "f": "פ", "q": "ק", "r": "ר", "t": "ת",
}


def value(char: str) -> int:
    """Return the gematric value of a single character (0 if unknown)."""
    char = char.lower()
    if char in HEBREW_VALUES:
        return HEBREW_VALUES[char]
    if char in LATIN_TO_HEBREW:
        return HEBREW_VALUES[LATIN_TO_HEBREW[char]]
    return 0


def sum_word(text: str) -> int:
    """
    Sum the gematric values of all characters in a word/string.
    Whitespace and unknown chars contribute 0.
    """
    return sum(value(c) for c in text)


def reduce(text: str) -> int:
    """Return the digital root of the gematria sum."""
    return digital_root(sum_word(text))


def fingerprint(text: str) -> dict:
    """All three readings in one shot — useful for content tagging."""
    s = sum_word(text)
    return {
        "text":         text,
        "sum":          s,
        "digital_root": digital_root(s),
        "char_count":   sum(1 for c in text if value(c) > 0),
    }
