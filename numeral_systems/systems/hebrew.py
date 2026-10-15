"""
Hebrew alphabetic numerals.

An ADDITIVE DECIMAL numeral system, adapted from the Greek Milesian system;
the earliest archaeological evidence is late second century BCE. Because the
Hebrew alphabet has 22 letters, the series stops at 400 rather than reaching
900 as the Greek does. Claim key: ``hebrew-from-greek``.

    units      alef 1  bet 2  gimel 3  dalet 4  he 5
               vav 6   zayin 7  het 8  tet 9
    tens       yod 10  kaf 20  lamed 30  mem 40  nun 50
               samekh 60  ayin 70  pe 80  tsadi 90
    hundreds   qof 100  resh 200  shin 300  tav 400

Values from 500 to 900 are built by repeating tav: 500 is tav-qof, 800 is
tav-tav, 900 is tav-tav-qof.

TWO CONVENTIONS WORTH KNOWING. Final (sofit) letter forms carry the same
value as their ordinary forms. And 15 and 16 are written tet-vav (9 + 6) and
tet-zayin (9 + 7) rather than yod-he and yod-vav, because those spellings
would form divine names. ``to_hebrew`` honours that rule; it is a real
property of the system, not an ornament.

Numerals are marked with geresh (U+05F3) for a single letter and gershayim
(U+05F4) before the last letter of a multi-letter numeral.

This module represents quantity. Gematria -- reading meaning from a word's
letter-sum -- is a different activity and lives in
``numeral_systems.interpretive``. Claim key: ``notation-is-not-interpretation``.
"""
from __future__ import annotations

GERESH = "׳"      # HEBREW PUNCTUATION GERESH
GERSHAYIM = "״"   # HEBREW PUNCTUATION GERSHAYIM

UNITS: dict[int, str] = {
    1: "א", 2: "ב", 3: "ג", 4: "ד", 5: "ה",
    6: "ו", 7: "ז", 8: "ח", 9: "ט",
}
TENS: dict[int, str] = {
    1: "י", 2: "כ", 3: "ל", 4: "מ", 5: "נ",
    6: "ס", 7: "ע", 8: "פ", 9: "צ",
}
HUNDREDS: dict[int, str] = {
    1: "ק", 2: "ר", 3: "ש", 4: "ת",
}

# Final forms carry their ordinary value.
FINAL_FORMS: dict[str, int] = {
    "ך": 20,   # kaf sofit
    "ם": 40,   # mem sofit
    "ן": 50,   # nun sofit
    "ף": 80,   # pe sofit
    "ץ": 90,   # tsadi sofit
}

VALUES: dict[str, int] = {}
for _rank, _scale in ((UNITS, 1), (TENS, 10), (HUNDREDS, 100)):
    for _digit, _char in _rank.items():
        VALUES[_char] = _digit * _scale
VALUES.update(FINAL_FORMS)

# The two spellings avoided because they form divine names.
AVOIDED = {15: (9, 6), 16: (9, 7)}

MAX_REPRESENTABLE = 999


def value(char: str) -> int:
    """The numeral value of one Hebrew letter, or 0 if it carries none."""
    if not char:
        return 0
    return VALUES.get(char, 0)


def to_hebrew(n: int) -> str:
    """Write ``n`` in Hebrew numerals, without geresh or gershayim.

    Hundreds above 400 repeat tav. The tet-vav and tet-zayin convention is
    applied for 15 and 16, including inside larger numbers such as 115.
    """
    if n < 1:
        raise ValueError(
            f"Hebrew numerals have no zero and no negatives; got {n}. "
            f"This module represents 1 through {MAX_REPRESENTABLE}."
        )
    if n > MAX_REPRESENTABLE:
        raise ValueError(
            f"{n} is above this module's range of 1 through "
            f"{MAX_REPRESENTABLE}. Thousands reuse the unit letters with "
            "their own marking, which this module does not implement."
        )
    out = ""
    hundreds, rest = divmod(n, 100)
    while hundreds > 4:
        out += HUNDREDS[4]
        hundreds -= 4
    if hundreds:
        out += HUNDREDS[hundreds]
    if rest in AVOIDED:
        tens_digit, units_digit = AVOIDED[rest]
        return out + UNITS[tens_digit] + UNITS[units_digit]
    tens, units = divmod(rest, 10)
    if tens:
        out += TENS[tens]
    if units:
        out += UNITS[units]
    return out


def from_hebrew(text: str) -> int:
    """Read a Hebrew numeral back to an integer.

    Geresh and gershayim are ignored. Characters carrying no numeral value
    are rejected by name rather than silently skipped.
    """
    total = 0
    for char in text:
        if char in (GERESH, GERSHAYIM):
            continue
        v = value(char)
        if v == 0:
            raise ValueError(
                f"{char!r} (U+{ord(char):04X}) carries no Hebrew numeral value."
            )
        total += v
    return total


def letter_sum(text: str) -> int:
    """The sum of the numeral values of every Hebrew letter in ``text``.

    An ORDER-INDEPENDENT sum: any rearrangement of the same letters gives
    the same result. This is the arithmetic gematria uses; the interpretive
    practice itself lives in ``numeral_systems.interpretive``.
    """
    return sum(value(c) for c in text)
