"""
Mesopotamian sexagesimal notation -- base 60, with a sub-base of 10.

A POSITIONAL system, unlike the three alphabetic systems in this package,
and the earliest positional notation known. Claim key:
``sexagesimal-positional``.

THE SUB-BASE. Each of the 59 non-zero digits is built from just two wedge
signs: one counting units and one counting tens. The digit 23 is two tens
wedges followed by three units wedges. So the system is base 60 at the level
of PLACES and base 10 inside each DIGIT. ``digit_wedges`` exposes that
structure directly.

NO ZERO. There was no true zero sign, so place value had to be inferred
from context, and the same marks could be read at different magnitudes.
Later scribes left a gap. This is a real limitation of the historical
system, not an artefact of this module -- which is why ``to_sexagesimal(0)``
returning a zero digit is a modern convenience and says so.

ON WHY BASE 60. It is often said the Mesopotamians chose 60 for its many
divisors. That is a plausible convenience and it is certainly why the base
SURVIVED in time and angle measure, but the historical origin is disputed:
one account derives it from the decimal lexical numerals of Semitic
languages, another from Sumerian practice. This module does not assert a
cause.

Sexagesimal is the one system here still in everyday use: 60 seconds to the
minute, 60 minutes to the degree, 360 degrees to the circle.

The primary material -- the mathematical tablets themselves -- is held
chiefly in the British Museum, the Louvre, and the Vorderasiatisches Museum
in Berlin. Claim key: ``sexagesimal-primary-material``.
"""
from __future__ import annotations
from dataclasses import dataclass

from ..primitives import to_base, from_base, sexagesimal_string

BASE = 60
SUB_BASE = 10


@dataclass(frozen=True)
class TimeTriple:
    """Hours, minutes, seconds -- the sexagesimal time form."""
    hours: int
    minutes: int
    seconds: int

    def __str__(self) -> str:
        return f"{self.hours:02d}:{self.minutes:02d}:{self.seconds:02d}"

    def total_seconds(self) -> int:
        return self.hours * 3600 + self.minutes * 60 + self.seconds


@dataclass(frozen=True)
class AngleTriple:
    """Degrees, arcminutes, arcseconds -- the sexagesimal angular form."""
    degrees: int
    arcmin: int
    arcsec: int

    def __str__(self) -> str:
        return f"{self.degrees}°{self.arcmin:02d}'{self.arcsec:02d}\""

    def total_arcseconds(self) -> int:
        return self.degrees * 3600 + self.arcmin * 60 + self.arcsec


def digit_wedges(digit: int) -> tuple[int, int]:
    """Decompose one sexagesimal digit into (tens wedges, units wedges).

    This is the sub-base of 10 made explicit: every digit from 0 to 59 is
    written with at most five tens wedges and nine units wedges.

        digit_wedges(23) -> (2, 3)
        digit_wedges(59) -> (5, 9)
    """
    if not 0 <= digit < BASE:
        raise ValueError(
            f"A sexagesimal digit runs 0 through {BASE - 1}; got {digit}."
        )
    return divmod(digit, SUB_BASE)


def wedge_layout(n: int) -> list[tuple[int, int]]:
    """Every place of ``n``, most significant first, as wedge counts."""
    return [digit_wedges(d) for d in to_base(n, BASE)]


def encode_time(total_seconds: int) -> TimeTriple:
    """Convert total seconds into an HH:MM:SS sexagesimal triple."""
    if total_seconds < 0:
        raise ValueError("encode_time requires non-negative seconds")
    hours, rem = divmod(total_seconds, 3600)
    minutes, seconds = divmod(rem, 60)
    return TimeTriple(hours, minutes, seconds)


def decode_time(triple: TimeTriple) -> int:
    """Convert an HH:MM:SS triple back to total seconds."""
    return triple.total_seconds()


def encode_angle(total_arcseconds: int) -> AngleTriple:
    """Convert total arcseconds into a degrees/arcmin/arcsec triple."""
    if total_arcseconds < 0:
        raise ValueError("encode_angle requires non-negative arcseconds")
    degrees, rem = divmod(total_arcseconds, 3600)
    arcmin, arcsec = divmod(rem, 60)
    return AngleTriple(degrees, arcmin, arcsec)


def decode_angle(triple: AngleTriple) -> int:
    """Convert a degrees/arcmin/arcsec triple back to total arcseconds."""
    return triple.total_arcseconds()


def to_sexagesimal(n: int) -> str:
    """Render an integer in place-separated sexagesimal, as '1,02,05'.

    A zero digit is written 0 here. The historical system had no zero sign
    and relied on context, so this is a modern reading convenience.
    """
    return sexagesimal_string(n)


def from_sexagesimal(s: str) -> int:
    """Parse place-separated sexagesimal back to an integer.

    ``from_sexagesimal('1,02,05')`` is 3725.
    """
    parts = [int(p) for p in s.split(",")]
    return from_base(parts, BASE)


def babylonian_fraction(numerator: int, denominator: int, places: int = 4) -> list[int]:
    """Express a fraction as sexagesimal places: sixtieths, then 3600ths.

        babylonian_fraction(1, 2, 1) -> [30]      (1/2 = 30/60)
        babylonian_fraction(1, 3, 2) -> [20, 0]   (1/3 = 20/60)

    A fraction whose denominator has a prime factor other than 2, 3 or 5
    does not terminate in base 60 and is truncated at ``places``.
    """
    if denominator <= 0:
        raise ValueError("denominator must be positive")
    if places < 1:
        raise ValueError("places must be at least 1")
    n = numerator * (BASE ** places) // denominator
    digits = to_base(n, BASE)
    while len(digits) < places:
        digits.insert(0, 0)
    return digits


def terminates(denominator: int) -> bool:
    """Whether 1/denominator terminates in base 60.

    True exactly when the denominator's only prime factors are 2, 3 and 5 --
    the primes dividing 60. This is the real reason base 60 is convenient
    for fractions, stated as a property rather than as a motive.
    """
    if denominator <= 0:
        raise ValueError("denominator must be positive")
    d = denominator
    for prime in (2, 3, 5):
        while d % prime == 0:
            d //= prime
    return d == 1


def fingerprint(n: int) -> dict:
    """Render an integer in each sexagesimal form this module supports."""
    time = encode_time(n)
    angle = encode_angle(n)
    return {
        "n": n,
        "sexagesimal": to_sexagesimal(n),
        "wedge_layout": wedge_layout(n),
        "time_form": str(time),
        "time_total_seconds": time.total_seconds(),
        "angle_form": str(angle),
        "angle_arcseconds": angle.total_arcseconds(),
    }
