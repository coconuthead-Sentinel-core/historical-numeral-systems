"""
classroom.py -- teaching material for each system in this library.

Every lesson names its claim keys, and ``tests/test_sources.py`` fails the
build if a key here has no entry in ``numeral_systems.sources``. A lesson
cannot assert something the register does not back.

Each lesson states what the system IS NOT, because that is where the
earlier version of this library went wrong: it described interpretive
practices as number systems and modern numerology as ancient.
"""
from __future__ import annotations

from . import sources

_LESSONS: dict[str, dict] = {
    "hebrew": {
        "system": "Hebrew alphabetic numerals",
        "type": "additive, decimal, non-positional",
        "period": "adapted from Greek; earliest evidence late 2nd c. BCE",
        "method": (
            "Nine units, nine tens, four hundreds, to 400. A number is "
            "the sum of its letters. Values above 400 repeat tav."
        ),
        "is_not": (
            "Not gematria. Gematria is an exegetical practice that uses "
            "these values; the numeral system is what the values ARE."
        ),
        "example": "from numeral_systems.systems import hebrew; hebrew.to_hebrew(241)",
        "exercise": (
            "Encode 15 and 16. Explain why the output is not yod-he and "
            "yod-vav, and what rule produced it instead."
        ),
        "claims": [
            "alphabetic-numerals-are-numeral-systems",
            "hebrew-from-greek",
            "notation-is-not-interpretation",
        ],
    },
    "greek": {
        "system": "Greek alphabetic (Milesian) numerals",
        "type": "additive, decimal, non-positional",
        "period": "attested from roughly the 6th c. BCE",
        "method": (
            "Twenty-seven values in three ranks of nine. The alphabet "
            "supplies only 24, so stigma, koppa and sampi carry 6, 90 "
            "and 900."
        ),
        "is_not": (
            "Not isopsephy, and not 'Pythagorean numerology'. The first "
            "is an interpretive use of these values; the second is a "
            "20th-century system wearing a classical name."
        ),
        "example": "from numeral_systems.systems import greek; greek.to_greek(900)",
        "exercise": (
            "Try to write 96 using only the 24 classical letters. Explain "
            "what fails, then do it with the full table."
        ),
        "claims": [
            "greek-milesian-structure",
            "greek-obsolete-letters",
            "pythagorean-label-is-borrowed",
            "notation-is-not-interpretation",
        ],
    },
    "arabic": {
        "system": "Arabic abjad numerals (eastern order)",
        "type": "additive, decimal, non-positional",
        "period": "in ordinary mathematical use before Hindu-Arabic numerals",
        "method": (
            "The 28 letters in old alphabetic order. Values match Hebrew "
            "to 400, then run 500 to 1000."
        ),
        "is_not": (
            "Not one single system. The Maghrebi order assigns several "
            "later letters different values, so a reading is only "
            "meaningful once the order is stated."
        ),
        "example": "from numeral_systems.systems import arabic; arabic.to_abjad(1443)",
        "exercise": (
            "Encode a year, decode it back, and confirm the round trip. "
            "Then say which order you used and why it matters."
        ),
        "claims": [
            "abjad-decimal-structure",
            "alphabetic-numerals-are-numeral-systems",
        ],
    },
    "sexagesimal": {
        "system": "Mesopotamian sexagesimal notation",
        "type": "POSITIONAL, base 60, sub-base 10",
        "period": "Bronze Age Mesopotamia; the earliest positional notation",
        "method": (
            "Places count in 60s. Inside each digit, two wedge signs "
            "count tens and units, which is the sub-base of 10."
        ),
        "is_not": (
            "Not an alphabetic system, and not complete: there was no "
            "zero sign, so magnitude had to come from context."
        ),
        "example": (
            "from numeral_systems.systems import sexagesimal; "
            "sexagesimal.digit_wedges(23)"
        ),
        "exercise": (
            "Use terminates() to find which unit fractions terminate in "
            "base 60. State the rule you discover in one sentence."
        ),
        "claims": ["sexagesimal-positional", "sexagesimal-primary-material"],
    },
    "chronograms": {
        "system": "Chronograms (madda tarikh)",
        "type": "an application of abjad values, not a system of its own",
        "period": (
            "letter values from the 12th c.; organised phrases from "
            "around the turn of the 14th"
        ),
        "method": (
            "Choose words whose abjad sum equals the year being recorded. "
            "Used for births, deaths, appointments, buildings, war and peace."
        ),
        "is_not": (
            "Not divination. A chronogram has a right answer -- the sum "
            "either equals the year or it does not."
        ),
        "example": "from numeral_systems import chronograms; chronograms.compose_hint(1121)",
        "exercise": (
            "Build the letter skeleton for a year, then verify() a phrase "
            "against it and read the delta."
        ),
        "claims": ["chronograms-attested", "chronogram-phrase-era"],
    },
    "readability": {
        "system": "Readability formulas",
        "type": "modern quantitative text measure",
        "period": "Flesch 1948; Flesch-Kincaid 1975",
        "method": (
            "Words per sentence and syllables per word, combined by a "
            "published formula into an ease score or a grade level."
        ),
        "is_not": (
            "Not cognitive load, which is a distinct construct from "
            "instructional-design research. Not Sanskrit prosody either, "
            "which is what an earlier version of this library called it."
        ),
        "example": "from numeral_systems import readability; readability.report('A short sentence.')",
        "exercise": (
            "Score two paragraphs of your own writing. Then explain why "
            "the syllable counter is wrong about the word 'poem'."
        ),
        "claims": ["readability-formulas-are-published"],
    },
}

# What this library used to compute and no longer does, with the reason.
RETIRED: dict[str, dict] = {
    "life_number / life_path_number": {
        "was_described_as": "classical, and assigned by Pythagoras",
        "finding": (
            "The name-and-birth-date method is early-20th-century and "
            "American, originating with L. Dow Balliett. The Pythagorean "
            "label is borrowed."
        ),
        "claims": ["life-path-is-modern", "pythagorean-label-is-borrowed"],
    },
    "soul_number / destiny_number": {
        "was_described_as": "Vedic readings; the Sanskrit 'akshara' destiny",
        "finding": (
            "No source supports these as Vedic or Sanskrit methods. The "
            "arithmetic was invented for the module."
        ),
        "claims": ["vedic-attribution-unsupported"],
    },
    "number_meaning (planetary)": {
        "was_described_as": "classical Vedic planetary correspondences",
        "finding": (
            "Unsupported in the scholarly record. The modern practice is "
            "best described as a synthesis of jyotish vocabulary, the "
            "Chinese Lo Shu grid, and Western name-number methods."
        ),
        "claims": ["vedic-attribution-unsupported"],
    },
    "complexity_score": {
        "was_described_as": "a cognitive load classifier",
        "finding": (
            "Readability is not cognitive load. The implementation also "
            "inverted its own bands and added the gematria sum modulo 7 "
            "as an arbitrary term."
        ),
        "claims": ["readability-formulas-are-published"],
    },
    "Latin transliteration tables": {
        "was_described_as": "standard Hebrew-to-Latin and Arabic mappings",
        "finding": (
            "Ad hoc and unsourced. Real romanization standards exist "
            "(ISO 259 for Hebrew, ISO 233 and DIN 31635 for Arabic); the "
            "tables matched none of them."
        ),
        "claims": ["alphabetic-numerals-are-numeral-systems"],
    },
}


def lesson(name: str) -> dict:
    """One lesson by key, or every lesson when ``name`` is 'all'."""
    if name == "all":
        return _LESSONS
    return _LESSONS.get(name.lower(), {"error": f"unknown lesson: {name}"})


def lesson_names() -> list[str]:
    """Every lesson key, in teaching order."""
    return list(_LESSONS)


def print_lesson(name: str) -> str:
    """Format one lesson as a plain-text block, citations included."""
    L = lesson(name)
    if "error" in L:
        return L["error"]
    lines = [
        f"=== {L['system']} ===",
        f"Type:      {L['type']}",
        f"Period:    {L['period']}",
        f"Method:    {L['method']}",
        f"Is NOT:    {L['is_not']}",
        f"Example:   {L['example']}",
        f"Exercise:  {L['exercise']}",
        "Sources:",
    ]
    seen: set[str] = set()
    for claim in L["claims"]:
        for src in sources.sources_for(claim):
            if src["key"] in seen:
                continue
            seen.add(src["key"])
            lines.append(f"  [{src['key']}] {src['text']}")
    return "\n".join(lines)


def print_all() -> str:
    """Every lesson, in teaching order."""
    return "\n\n".join(print_lesson(name) for name in _LESSONS)


def print_retired() -> str:
    """The record of what was removed on verification, and why."""
    lines = ["=== Retired on verification ==="]
    for name, entry in RETIRED.items():
        lines.append(f"\n{name}")
        lines.append(f"  was described as: {entry['was_described_as']}")
        lines.append(f"  finding:          {entry['finding']}")
    return "\n".join(lines)


def all_claim_keys() -> list[str]:
    """Every claim key referenced by the lessons and the retired record."""
    keys: set[str] = set()
    for entry in _LESSONS.values():
        keys.update(entry["claims"])
    for entry in RETIRED.values():
        keys.update(entry["claims"])
    return sorted(keys)
