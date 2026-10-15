"""
readability.py -- syllable counting and published readability formulas.

This module has no historical claim attached to it. It exists because an
earlier version of this library counted syllables under the heading of
Sanskrit prosody and then fed the count into a score it called cognitive
load. Neither label was earned: the counter is an English heuristic, and
cognitive load is a specific construct from instructional-design research
that a syllable count does not measure.

What a syllable count DOES support is readability, and readability has
published formulas with names, authors and dates. Those are implemented
here. Claim key: ``readability-formulas-are-published``.

THE COUNTER IS A HEURISTIC AND WILL BE WRONG. It counts vowel clusters and
then subtracts a silent trailing 'e'. It is reliable in aggregate over a
paragraph and unreliable on any single word: it undercounts 'poem' and
'idea', and English spelling guarantees a long tail of failures. It is not
a pronunciation dictionary and does not pretend to be. For exact counts,
use a phonetic lexicon.
"""
from __future__ import annotations
import re

VOWELS = set("aeiouy")

_WORD = re.compile(r"[A-Za-z']+")
_SENTENCE_END = re.compile(r"[.!?]+")


def syllable_count(text: str) -> int:
    """Approximate English syllable count by vowel clusters.

    Every word scores at least 1. See the module docstring for the known
    failure modes before relying on a single-word result.
    """
    count = 0
    for word in _WORD.findall(text.lower()):
        clusters = 0
        prev_vowel = False
        for char in word:
            is_vowel = char in VOWELS
            if is_vowel and not prev_vowel:
                clusters += 1
            prev_vowel = is_vowel
        if word.endswith("e") and clusters > 1:
            clusters -= 1
        count += max(1, clusters)
    return count


def word_count(text: str) -> int:
    """Words, by the same token pattern the syllable counter uses."""
    return len(_WORD.findall(text))


def sentence_count(text: str) -> int:
    """Sentences, by terminal punctuation.

    Returns at least 1 for any text containing a word, since the
    readability formulas divide by this. Text with no terminal punctuation
    is treated as one sentence -- which inflates the difficulty score, so
    the caller should know whether its input is punctuated.
    """
    if not _WORD.search(text):
        return 0
    found = len([s for s in _SENTENCE_END.findall(text) if s])
    return max(1, found)


def flesch_reading_ease(text: str) -> float | None:
    """Flesch Reading Ease. Higher is easier; roughly 0 to 100.

    Flesch, Rudolf. 'A New Readability Yardstick.' Journal of Applied
    Psychology 32, no. 3 (1948): 221-33.

    Returns None for text with no words, rather than raising or inventing
    a score.
    """
    words = word_count(text)
    if words == 0:
        return None
    sentences = sentence_count(text)
    syllables = syllable_count(text)
    return round(
        206.835 - 1.015 * (words / sentences) - 84.6 * (syllables / words), 2
    )


def flesch_kincaid_grade(text: str) -> float | None:
    """Flesch-Kincaid Grade Level -- a US school grade. Higher is harder.

    Kincaid, J. Peter, et al. 'Derivation of New Readability Formulas for
    Navy Enlisted Personnel.' Naval Technical Training Command, Research
    Branch Report 8-75, 1975.

    Returns None for text with no words.
    """
    words = word_count(text)
    if words == 0:
        return None
    sentences = sentence_count(text)
    syllables = syllable_count(text)
    return round(
        0.39 * (words / sentences) + 11.8 * (syllables / words) - 15.59, 2
    )


def difficulty_band(text: str) -> str | None:
    """A three-way reading-difficulty band from the grade level.

        grade below 6      -> 'EASY'
        grade 6 to 12      -> 'MODERATE'
        grade above 12     -> 'HARD'

    Oriented so that HARDER TEXT GIVES A HARDER BAND. An earlier version of
    this library inverted that, returning its most permissive label for its
    most complex input. Returns None for text with no words.

    This is reading difficulty. It is not a measure of cognitive load, and
    mapping it onto another system's zone colours is the caller's decision,
    not this function's.
    """
    grade = flesch_kincaid_grade(text)
    if grade is None:
        return None
    if grade < 6:
        return "EASY"
    if grade <= 12:
        return "MODERATE"
    return "HARD"


def report(text: str) -> dict:
    """Every measure in this module for one piece of text."""
    return {
        "text": text,
        "words": word_count(text),
        "sentences": sentence_count(text),
        "syllables": syllable_count(text),
        "flesch_reading_ease": flesch_reading_ease(text),
        "flesch_kincaid_grade": flesch_kincaid_grade(text),
        "difficulty_band": difficulty_band(text),
    }
