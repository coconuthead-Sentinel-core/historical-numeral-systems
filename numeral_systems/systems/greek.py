"""
Greek alphabetic numerals -- the Milesian (also Ionian, Alexandrian) system.

An ADDITIVE DECIMAL numeral system. Twenty-seven letter values in three
ranks of nine:

    units      a 1   b 2   g 3   d 4   e 5   STIGMA 6   z 7   e 8   th 9
    tens       i 10  k 20  l 30  m 40  n 50  x 60  o 70  p 80  KOPPA 90
    hundreds   r 100 s 200 t 300 u 400 ph 500 ch 600 ps 700 o 800 SAMPI 900

A number is the SUM of its letters, so 241 is written sigma-mu-alpha
(200 + 40 + 1). Claim key: ``greek-milesian-structure``.

THE THREE EXTRA LETTERS. The classical Greek alphabet has 24 letters and
this system needs 27, so three letters outside it carry 6, 90 and 900:
stigma, koppa and sampi. They survive almost solely as numerals. Omitting
them does not merely lose three glyphs -- it makes 6, 90, 900 and every
number containing them unrepresentable. Claim key:
``greek-obsolete-letters``.

Numerals are marked off from words by the keraia, U+0374. Thousands reuse
the unit letters with the lower numeral sign U+0375 in front.

This module represents quantity. The interpretive practice of reading
meaning from a word's letter-sum -- isopsephy -- is a different activity
and lives in ``numeral_systems.interpretive``. Claim key:
``notation-is-not-interpretation``.
"""
from __future__ import annotations

# Numeral-only letters, by Unicode code point.
STIGMA = "ϛ"          # GREEK SMALL LETTER STIGMA -- 6
DIGAMMA = "ϝ"         # GREEK SMALL LETTER DIGAMMA -- 6, archaic form
KOPPA = "ϟ"           # GREEK SMALL LETTER KOPPA -- 90
ARCHAIC_KOPPA = "ϙ"   # GREEK SMALL LETTER ARCHAIC KOPPA -- 90
SAMPI = "ϡ"           # GREEK SMALL LETTER SAMPI -- 900
ARCHAIC_SAMPI = "ͳ"   # GREEK SMALL LETTER ARCHAIC SAMPI -- 900

KERAIA = "ʹ"          # GREEK NUMERAL SIGN -- marks a numeral
LOWER_KERAIA = "͵"    # GREEK LOWER NUMERAL SIGN -- marks thousands

# The canonical forms used when ENCODING a number.
UNITS: dict[int, str] = {
    1: "α", 2: "β", 3: "γ", 4: "δ", 5: "ε",
    6: STIGMA,   7: "ζ", 8: "η", 9: "θ",
}
TENS: dict[int, str] = {
    1: "ι", 2: "κ", 3: "λ", 4: "μ", 5: "ν",
    6: "ξ", 7: "ο", 8: "π", 9: KOPPA,
}
HUNDREDS: dict[int, str] = {
    1: "ρ", 2: "σ", 3: "τ", 4: "υ", 5: "φ",
    6: "χ", 7: "ψ", 8: "ω", 9: SAMPI,
}

# Every form accepted when DECODING, including variants and final sigma.
VALUES: dict[str, int] = {}
for _rank, _scale in ((UNITS, 1), (TENS, 10), (HUNDREDS, 100)):
    for _digit, _char in _rank.items():
        VALUES[_char] = _digit * _scale
VALUES[DIGAMMA] = 6
VALUES[ARCHAIC_KOPPA] = 90
VALUES[ARCHAIC_SAMPI] = 900
VALUES["ς"] = 200          # final sigma, same value as sigma

MAX_REPRESENTABLE = 9999


def value(char: str) -> int:
    """The Milesian value of one character, or 0 if it carries none.

    Accepts upper or lower case and the archaic variants of the three
    numeral-only letters.
    """
    if not char:
        return 0
    return VALUES.get(char.lower(), 0)


def to_greek(n: int) -> str:
    """Write ``n`` in Milesian numerals, without the keraia.

    Thousands take the lower numeral sign, so 1000 is lower-keraia alpha
    and 1998 is lower-keraia alpha, then 900 + 90 + 8.

        to_greek(241) -> 'sigma mu alpha'
        to_greek(6)   -> stigma
        to_greek(90)  -> koppa
        to_greek(900) -> sampi
    """
    if n < 1:
        raise ValueError(
            f"Milesian numerals have no zero and no negatives; got {n}. "
            "The system represents 1 through "
            f"{MAX_REPRESENTABLE} inclusive."
        )
    if n > MAX_REPRESENTABLE:
        raise ValueError(
            f"{n} is above this module's range. Milesian notation handles "
            f"1 through {MAX_REPRESENTABLE} with the lower numeral sign "
            "for thousands; larger values used a myriad notation this "
            "module does not implement."
        )
    out = ""
    thousands, rest = divmod(n, 1000)
    if thousands:
        out += LOWER_KERAIA + UNITS[thousands]
    hundreds, rest = divmod(rest, 100)
    if hundreds:
        out += HUNDREDS[hundreds]
    tens, units = divmod(rest, 10)
    if tens:
        out += TENS[tens]
    if units:
        out += UNITS[units]
    return out


def from_greek(text: str) -> int:
    """Read a Milesian numeral back to an integer.

    Keraia marks are ignored, except that the lower numeral sign
    multiplies the letter that follows it by 1000. Characters carrying no
    numeral value are rejected by name rather than silently skipped.
    """
    total = 0
    thousands_next = False
    for char in text:
        if char == KERAIA:
            continue
        if char == LOWER_KERAIA:
            thousands_next = True
            continue
        v = value(char)
        if v == 0:
            raise ValueError(
                f"{char!r} (U+{ord(char):04X}) carries no Milesian value. "
                "If this is meant to be 6, 90 or 900, use stigma "
                "(U+03DB), koppa (U+03DF) or sampi (U+03E1)."
            )
        if thousands_next:
            if v > 9:
                raise ValueError(
                    "The lower numeral sign may only precede a unit "
                    f"letter (1-9); {char!r} is worth {v}."
                )
            total += v * 1000
            thousands_next = False
        else:
            total += v
    if thousands_next:
        raise ValueError("Trailing lower numeral sign with no letter after it.")
    return total


def psephos(text: str) -> int:
    """The sum of the Milesian values of every letter in ``text``.

    *Psephos* means pebble-count. This is an ORDER-INDEPENDENT sum: any
    rearrangement of the same letters gives the same result. That makes it
    useless as a content fingerprint and is the property isopsephy relies
    on. See ``numeral_systems.interpretive``.
    """
    return sum(value(c) for c in text)
