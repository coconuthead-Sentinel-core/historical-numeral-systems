"""
Indian/Vedic numerology — number symbolism + syllable counting.

Vedic numerology assigns meaning to numbers 1-9 (planetary correspondences).
Syllable counting is foundational to Sanskrit prosody (chhanda).

This module provides:
  - syllable_count: approximate syllable count of any text (English heuristic)
  - life_number / destiny_number / soul_number: classical Vedic readings
  - number_meaning: planetary/qualitative correspondence per number
"""
from __future__ import annotations
import re
from ..primitives import digital_root


VOWELS = set("aeiouy")

NUMBER_MEANINGS = {
    1: {"planet": "Sun",       "quality": "leadership / origination"},
    2: {"planet": "Moon",      "quality": "duality / reception"},
    3: {"planet": "Jupiter",   "quality": "expansion / wisdom"},
    4: {"planet": "Rahu",      "quality": "structure / foundation"},
    5: {"planet": "Mercury",   "quality": "adaptation / communication"},
    6: {"planet": "Venus",     "quality": "harmony / aesthetics"},
    7: {"planet": "Ketu",      "quality": "introspection / mysticism"},
    8: {"planet": "Saturn",    "quality": "discipline / karma"},
    9: {"planet": "Mars",      "quality": "action / completion"},
}


def syllable_count(text: str) -> int:
    """
    Approximate English syllable count using vowel-cluster heuristic.
    Crude but useful for relative complexity scoring.
    """
    text = text.lower()
    count = 0
    for word in re.findall(r"[a-z']+", text):
        # Count vowel clusters
        prev_vowel = False
        word_count = 0
        for char in word:
            is_vowel = char in VOWELS
            if is_vowel and not prev_vowel:
                word_count += 1
            prev_vowel = is_vowel
        # Silent 'e' adjustment
        if word.endswith("e") and word_count > 1:
            word_count -= 1
        # Every word has at least 1 syllable
        word_count = max(1, word_count)
        count += word_count
    return count


def life_number(text: str) -> int:
    """
    Sum each character's mod-9 position, then reduce.
    For a name, this is the classical 'life path number'.
    """
    total = sum(((ord(c) - ord("a")) % 9) + 1 for c in text.lower() if "a" <= c <= "z")
    return digital_root(total) if total > 0 else 0


def destiny_number(text: str) -> int:
    """
    Sum syllable count + character count, reduce.
    Approximates the Sanskrit 'akshara' (syllable) destiny.
    """
    return digital_root(syllable_count(text) + len(re.findall(r"[a-zA-Z]", text)))


def soul_number(text: str) -> int:
    """
    Sum vowel values only (the Vedic "soul / inner self" reading).
    """
    total = sum(((ord(c) - ord("a")) % 9) + 1 for c in text.lower() if c in VOWELS)
    return digital_root(total) if total > 0 else 0


def number_meaning(n: int) -> dict:
    """Return planetary + quality correspondence for a number 1-9."""
    return NUMBER_MEANINGS.get(digital_root(n), {"planet": "?", "quality": "?"})


def fingerprint(text: str) -> dict:
    life = life_number(text)
    destiny = destiny_number(text)
    soul = soul_number(text)
    return {
        "text":              text,
        "syllable_count":    syllable_count(text),
        "life_number":       life,
        "destiny_number":    destiny,
        "soul_number":       soul,
        "life_meaning":      number_meaning(life) if life else None,
        "destiny_meaning":   number_meaning(destiny) if destiny else None,
        "soul_meaning":      number_meaning(soul) if soul else None,
    }
