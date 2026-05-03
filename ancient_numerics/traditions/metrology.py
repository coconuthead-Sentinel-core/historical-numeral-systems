"""
Mesopotamian metrology — base-60 (sexagesimal) arithmetic.

The Sumerians/Babylonians used base 60 because 60 is the smallest number
divisible by 1, 2, 3, 4, 5, and 6 — making it ideal for fractional work.
We still use sexagesimal for time (60 sec/min, 60 min/hr) and angles
(60 minutes/degree, 60 seconds/minute).

This module provides:
  - sexagesimal encoding/decoding
  - hours/minutes/seconds <-> seconds
  - degrees/arcminutes/arcseconds <-> total arcseconds
  - Babylonian fractional notation (using 1/60ths)
"""
from __future__ import annotations
from dataclasses import dataclass
from ..primitives import to_base, from_base, sexagesimal_string


@dataclass(frozen=True)
class TimeTriple:
    """Hours, minutes, seconds — the sexagesimal time form."""
    hours:    int
    minutes:  int
    seconds:  int

    def __str__(self) -> str:
        return f"{self.hours:02d}:{self.minutes:02d}:{self.seconds:02d}"

    def total_seconds(self) -> int:
        return self.hours * 3600 + self.minutes * 60 + self.seconds


@dataclass(frozen=True)
class AngleTriple:
    """Degrees, arcminutes, arcseconds — the sexagesimal angular form."""
    degrees:    int
    arcmin:     int
    arcsec:     int

    def __str__(self) -> str:
        return f"{self.degrees}°{self.arcmin:02d}'{self.arcsec:02d}\""

    def total_arcseconds(self) -> int:
        return self.degrees * 3600 + self.arcmin * 60 + self.arcsec


def encode_time(total_seconds: int) -> TimeTriple:
    """Convert total seconds into HH:MM:SS sexagesimal triple."""
    if total_seconds < 0:
        raise ValueError("encode_time requires non-negative seconds")
    hours, rem = divmod(total_seconds, 3600)
    minutes, seconds = divmod(rem, 60)
    return TimeTriple(hours, minutes, seconds)


def decode_time(triple: TimeTriple) -> int:
    """Convert HH:MM:SS triple back to total seconds."""
    return triple.total_seconds()


def encode_angle(total_arcseconds: int) -> AngleTriple:
    """Convert total arcseconds into degrees / arcmin / arcsec triple."""
    if total_arcseconds < 0:
        raise ValueError("encode_angle requires non-negative arcseconds")
    degrees, rem = divmod(total_arcseconds, 3600)
    arcmin, arcsec = divmod(rem, 60)
    return AngleTriple(degrees, arcmin, arcsec)


def decode_angle(triple: AngleTriple) -> int:
    return triple.total_arcseconds()


def to_sexagesimal(n: int) -> str:
    """Render any integer in classical Babylonian sexagesimal notation."""
    return sexagesimal_string(n)


def from_sexagesimal(s: str) -> int:
    """
    Parse a Babylonian sexagesimal string back to integer.
    from_sexagesimal('1,02,05') -> 3725
    """
    parts = [int(p) for p in s.split(",")]
    return from_base(parts, 60)


def babylonian_fraction(numerator: int, denominator: int, places: int = 4) -> list[int]:
    """
    Express a fraction as Babylonian sexagesimal places (1/60, 1/3600, ...).
    Returns the integer-coefficient list.

    babylonian_fraction(1, 2, 1) -> [30]   (1/2 = 30/60)
    babylonian_fraction(1, 3, 2) -> [20, 0] (1/3 = 20/60 + 0/3600)
    """
    if denominator <= 0:
        raise ValueError("denominator must be positive")
    out: list[int] = []
    n = numerator * (60 ** places)
    n //= denominator
    digits = to_base(n, 60)
    # Pad to 'places' length
    while len(digits) < places:
        digits.insert(0, 0)
    return digits


def fingerprint(n: int) -> dict:
    """Render an integer in all classical sexagesimal forms."""
    time = encode_time(n)
    angle = encode_angle(n)
    return {
        "n":                  n,
        "sexagesimal":        to_sexagesimal(n),
        "time_form":          str(time),
        "time_total_seconds": time.total_seconds(),
        "angle_form":         str(angle),
        "angle_arcseconds":   angle.total_arcseconds(),
    }
