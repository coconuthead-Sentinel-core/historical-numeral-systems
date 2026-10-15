"""
chronograms.py -- recording a date inside a word or phrase.

A chronogram encodes a year in the abjad values of a text: choose words
whose letter-sum equals the year you mean to record. The practice is well
attested in Persian and Urdu literature, where it is called *madda tarikh*.
Claim key: ``chronograms-attested``.

HOW IT DEVELOPED. Early poets wrote years out in words. Later they used
abjad letter values, at first treating letters as separate number-words --
Mas'ud-e Sa'd-e Salman, who died in 1121, encoded the year 469 AH that way.
From around the turn of the 14th century poets organised abjad values into
meaningful words and phrases, a technique called *hisab al-jummal*. Claim
key: ``chronogram-phrase-era``.

WHAT IT WAS USED FOR. Births, deaths, appointments and dismissals,
marriages, the construction of notable buildings, war and peace. Epitaph
chronograms are still being catalogued.

WHY IT SITS APART FROM INTERPRETATION. A chronogram has a right answer. The
sum either equals the year or it does not, and the poet either hit it or
missed. That makes it checkable in a way gematria and isopsephy are not,
which is why it has its own module rather than living in
``numeral_systems.interpretive``.

ERAS. Chronograms in this tradition record Hijri (AH) years. Converting AH
to CE exactly requires a calendar implementation this module does not
carry, because the Hijri year is lunar and runs about eleven days shorter
than the solar year. ``approximate_ce`` is offered for orientation only and
says so in its name.
"""
from __future__ import annotations

from .systems import arabic

# The era a chronogram's year is assumed to be in, unless stated otherwise.
DEFAULT_ERA = "AH"


def verify(text: str, year: int, era: str = DEFAULT_ERA) -> dict:
    """Check whether ``text`` is a chronogram for ``year``.

    Returns the letter-sum, whether it matches, and by how much it misses.
    A miss is reported as a signed delta rather than a bare False, because
    the near-misses are what a poet actually works with.
    """
    total = arabic.letter_sum(text)
    return {
        "text": text,
        "letter_sum": total,
        "target_year": year,
        "era": era,
        "matches": total == year,
        "delta": total - year,
        "order": arabic.ORDER,
    }


def candidates(wordlist: list[str], year: int) -> list[str]:
    """Every entry of ``wordlist`` whose abjad sum equals ``year``.

    This library ships no lexicon -- supplying the word list is the
    caller's job, and the choice of lexicon is a scholarly decision rather
    than a default this module should make.
    """
    return [w for w in wordlist if arabic.letter_sum(w) == year]


def approximate_ce(hijri_year: int) -> int:
    """A rough CE year for a Hijri year. ORIENTATION ONLY.

    Uses the common approximation CE = AH + 622 - (AH / 33), which reflects
    the lunar year's drift against the solar one. It can be a year out, and
    it says nothing about which month. For a real conversion use a calendar
    library; for scholarly work use the tables.
    """
    if hijri_year < 1:
        raise ValueError(f"Hijri years start at 1; got {hijri_year}.")
    return int(hijri_year + 622 - (hijri_year / 33))


def compose_hint(year: int) -> dict:
    """What a chronogram for ``year`` would have to add up to, by place.

    Decomposes the target into the abjad letters that would sum to it --
    the skeleton a poet then has to find real words around.
    """
    if year < 1:
        raise ValueError(f"A chronogram year must be positive; got {year}.")
    skeleton = arabic.to_abjad(year)
    return {
        "target_year": year,
        "letter_skeleton": skeleton,
        "letter_values": [arabic.value(c) for c in skeleton],
        "checks_back_to": arabic.from_abjad(skeleton),
        "order": arabic.ORDER,
    }
