"""
classroom.py — printable explainers for each tradition.

Useful for documentation, teaching, or a CLI 'help' command.
Maps the historical context to the modern CS analog for each tradition.
"""
from __future__ import annotations


_LESSONS = {
    "gematria": {
        "tradition":      "Hebrew Gematria",
        "origin":         "Late antiquity; codified in Kabbalah",
        "core_method":    "Each Hebrew letter has a numeric value (1, 2, ..., 400). Sum the letters of a word.",
        "modern_analog":  "Character->integer hash + sum: a deterministic content fingerprint.",
        "code_example":   "from ancient_numerics.traditions import gematria; gematria.sum_word('hello')",
        "exercise":       "Verify: word A and its anagram have the same gematria sum.",
    },
    "isopsephy": {
        "tradition":      "Greek Isopsephy / Pythagorean Numerology",
        "origin":         "Classical Greece; Pythagorean school, ~6th c BCE",
        "core_method":    "Greek Milesian alphabet has positional values; sum gives 'psephos'. Modern Pythagorean reduces Latin chars mod 9.",
        "modern_analog":  "Weighted positional hashing — same principle as polynomial rolling hash.",
        "code_example":   "from ancient_numerics.traditions import isopsephy; isopsephy.psephos('logos')",
        "exercise":       "Compute the life path number of your name; compare to Pythagoras's correspondences.",
    },
    "abjad": {
        "tradition":      "Arabic Abjad",
        "origin":         "Early Islamic period (~7th c CE)",
        "core_method":    "Each letter has a value (1-1000). Sum a word; if the sum equals a year, the word is a 'chronogram' for that year.",
        "modern_analog":  "Date encoding via word selection — like MAC address vanity strings or PGP fingerprints with mnemonic hex.",
        "code_example":   "from ancient_numerics.traditions import abjad; abjad.chronogram('text', 1442)",
        "exercise":       "Find a word/phrase whose abjad sum equals the current year.",
    },
    "vedic": {
        "tradition":      "Indian / Vedic Numerology",
        "origin":         "Ancient South Asia; foundational to Sanskrit prosody",
        "core_method":    "Numbers 1-9 have planetary correspondences. Syllable count drives Sanskrit meter (chhanda).",
        "modern_analog":  "Tokenization heuristics + complexity scoring — what NLP libraries do for readability metrics.",
        "code_example":   "from ancient_numerics.traditions import vedic; vedic.syllable_count('beautiful')",
        "exercise":       "Compute syllable count of a Sanskrit shloka; verify it matches the prescribed meter.",
    },
    "metrology": {
        "tradition":      "Mesopotamian Sexagesimal",
        "origin":         "Bronze Age Mesopotamia (~3000 BCE); Sumerian/Babylonian",
        "core_method":    "Base-60 numbers (60 has many factors: 1,2,3,4,5,6,10,12,15,20,30,60).",
        "modern_analog":  "We still use it: 60 sec/min, 60 min/hr, 360°. Also: alternate-base arithmetic in number theory.",
        "code_example":   "from ancient_numerics.traditions import metrology; metrology.to_sexagesimal(3725)",
        "exercise":       "Verify: any common fraction (1/2, 1/3, 1/4, 1/5, 1/6) has a clean sexagesimal representation.",
    },
}


def lesson(name: str) -> dict:
    """Return the lesson dict for one tradition (or all if name is 'all')."""
    if name == "all":
        return _LESSONS
    return _LESSONS.get(name.lower(), {"error": f"unknown tradition: {name}"})


def print_lesson(name: str) -> str:
    """Format a lesson as a readable plain-text block."""
    L = lesson(name)
    if "error" in L:
        return L["error"]
    lines = [f"=== {L['tradition']} ===",
             f"Origin:        {L['origin']}",
             f"Core method:   {L['core_method']}",
             f"Modern analog: {L['modern_analog']}",
             f"Code example:  {L['code_example']}",
             f"Exercise:      {L['exercise']}"]
    return "\n".join(lines)


def print_all() -> str:
    """All five traditions, one after another."""
    return "\n\n".join(print_lesson(t) for t in ["gematria", "isopsephy", "abjad", "vedic", "metrology"])
