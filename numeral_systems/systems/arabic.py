"""
Arabic abjad numerals.

An ADDITIVE DECIMAL numeral system using the 28 Arabic letters in their old
alphabetic (abjad) order rather than the modern dictionary order. The values
match the Hebrew series up to 400; the extra Arabic letters then carry 500
through 1000. Claim key: ``abjad-decimal-structure``.

Before Hindu-Arabic positional numerals displaced it, the abjad served
ordinary mathematical use. It survives today chiefly for list and outline
numbering, and for chronograms (see ``numeral_systems.chronograms``).

TWO ORDERS EXIST. This module implements the EASTERN (mashriqi) order, which
is the one Persian and Urdu literature follows and the one chronogram
scholarship assumes. The Maghrebi order of North Africa and al-Andalus
assigns several of the later letters different values. Mixing the two
silently would corrupt any date reading, so this module implements one order
and says which.

Notation follows the script, right to left.

This module represents quantity. Reading meaning from a letter-sum is a
different activity; see ``numeral_systems.interpretive``. Claim key:
``notation-is-not-interpretation``.
"""
from __future__ import annotations

ORDER = "eastern"

# Eastern (mashriqi) abjad values.
VALUES: dict[str, int] = {
    "ا": 1,     # alif
    "ب": 2,     # ba
    "ج": 3,     # jim
    "د": 4,     # dal
    "ه": 5,     # ha
    "و": 6,     # waw
    "ز": 7,     # zay
    "ح": 8,     # ha (hah)
    "ط": 9,     # ta (tah)
    "ي": 10,    # ya
    "ك": 20,    # kaf
    "ل": 30,    # lam
    "م": 40,    # mim
    "ن": 50,    # nun
    "س": 60,    # sin
    "ع": 70,    # ayn
    "ف": 80,    # fa
    "ص": 90,    # sad
    "ق": 100,   # qaf
    "ر": 200,   # ra
    "ش": 300,   # shin
    "ت": 400,   # ta
    "ث": 500,   # tha
    "خ": 600,   # kha
    "ذ": 700,   # dhal
    "ض": 800,   # dad
    "ظ": 900,   # za (zah)
    "غ": 1000,  # ghayn
}

# Orthographic variants that carry the value of their base letter.
VARIANTS: dict[str, str] = {
    "أ": "ا",   # alif with hamza above
    "إ": "ا",   # alif with hamza below
    "آ": "ا",   # alif with madda
    "ٱ": "ا",   # alif wasla
    "ى": "ي",   # alif maqsura, counted as ya
    "ة": "ه",   # ta marbuta, counted as ha
}

# The order's traditional mnemonic words.
MNEMONIC = (
    "أبجد هوز حطي "
    "كلمن سعفص "
    "قرشت ثخذ ضظغ"
)

UNITS = {v: k for k, v in VALUES.items() if 1 <= v <= 9}
TENS = {v: k for k, v in VALUES.items() if 10 <= v <= 90}
HUNDREDS = {v: k for k, v in VALUES.items() if 100 <= v <= 900}
THOUSAND = "غ"

MAX_REPRESENTABLE = 9999


def value(char: str) -> int:
    """The abjad value of one character, or 0 if it carries none.

    Orthographic variants of alif, ya and ha resolve to their base letter.
    """
    if not char:
        return 0
    if char in VALUES:
        return VALUES[char]
    base = VARIANTS.get(char)
    return VALUES.get(base, 0) if base else 0


def to_abjad(n: int) -> str:
    """Write ``n`` in eastern abjad numerals.

    Thousands repeat ghayn, so 2000 is two ghayn. Letters are emitted from
    the largest value down; rendering right to left is the display layer's
    business, not this function's.
    """
    if n < 1:
        raise ValueError(
            f"Abjad numerals have no zero and no negatives; got {n}. "
            f"This module represents 1 through {MAX_REPRESENTABLE}."
        )
    if n > MAX_REPRESENTABLE:
        raise ValueError(
            f"{n} is above this module's range of 1 through "
            f"{MAX_REPRESENTABLE}."
        )
    out = ""
    thousands, rest = divmod(n, 1000)
    out += THOUSAND * thousands
    hundreds, rest = divmod(rest, 100)
    if hundreds:
        out += HUNDREDS[hundreds * 100]
    tens, units = divmod(rest, 10)
    if tens:
        out += TENS[tens * 10]
    if units:
        out += UNITS[units]
    return out


def from_abjad(text: str) -> int:
    """Read an abjad numeral back to an integer.

    Spaces and Arabic tatweel are ignored. Characters carrying no abjad
    value are rejected by name rather than silently skipped.
    """
    total = 0
    for char in text:
        if char.isspace() or char == "ـ":   # tatweel
            continue
        v = value(char)
        if v == 0:
            raise ValueError(
                f"{char!r} (U+{ord(char):04X}) carries no abjad value in "
                f"the {ORDER} order."
            )
        total += v
    return total


def letter_sum(text: str) -> int:
    """The sum of the abjad values of every letter in ``text``.

    An ORDER-INDEPENDENT sum. This is the arithmetic a chronogram rests on;
    see ``numeral_systems.chronograms``.
    """
    return sum(value(c) for c in text)
