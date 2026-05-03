"""
Greek Isopsephy / Pythagorean — letter values matching the Greek alphabet.

Standard Milesian numeral system (used by Pythagoras, Plato, classical Greek):
    α=1  β=2  γ=3  δ=4  ε=5  ζ=7  η=8  θ=9
    ι=10 κ=20 λ=30 μ=40 ν=50 ξ=60 ο=70 π=80
    ρ=100 σ=200 τ=300 υ=400 φ=500 χ=600 ψ=700 ω=800

Modern Pythagorean (Latin alphabet, 1-9 cycle): a=1, b=2, ..., i=9, j=1, etc.
"""
from __future__ import annotations
from ..primitives import digital_root, weighted_sum


GREEK_VALUES = {
    "α": 1,   "β": 2,   "γ": 3,   "δ": 4,   "ε": 5,
    "ζ": 7,   "η": 8,   "θ": 9,
    "ι": 10,  "κ": 20,  "λ": 30,  "μ": 40,  "ν": 50,
    "ξ": 60,  "ο": 70,  "π": 80,
    "ρ": 100, "σ": 200, "ς": 200, "τ": 300, "υ": 400,
    "φ": 500, "χ": 600, "ψ": 700, "ω": 800,
}


def pythagorean_value(char: str) -> int:
    """Modern Pythagorean: a=1, b=2, ..., i=9, j=1, k=2, ..., r=9, s=1, ..., z=8."""
    c = char.lower()
    if "a" <= c <= "z":
        return ((ord(c) - ord("a")) % 9) + 1
    return 0


def greek_value(char: str) -> int:
    """Classical Greek Milesian value (returns 0 for non-Greek)."""
    return GREEK_VALUES.get(char.lower(), 0)


def value(char: str) -> int:
    """
    Return whichever value (Greek or Pythagorean) is meaningful.
    Greek takes priority; falls back to Pythagorean for Latin chars.
    """
    g = greek_value(char)
    if g > 0:
        return g
    return pythagorean_value(char)


def psephos(text: str) -> int:
    """The 'psephos' (pebble count) — the sum value of a word."""
    return sum(value(c) for c in text)


def reduce(text: str) -> int:
    """Pythagorean reduction: psephos → digital root."""
    return digital_root(psephos(text))


def life_path_number(text: str) -> int:
    """
    Pythagorean 'life path' number — what Pythagoras assigned to a name.
    Returns digital root of the Pythagorean (mod-9) sum.
    """
    pythagorean_sum = sum(pythagorean_value(c) for c in text)
    return digital_root(pythagorean_sum)


def fingerprint(text: str) -> dict:
    """Full reading of a word in both Greek and Pythagorean systems."""
    return {
        "text":              text,
        "greek_psephos":     sum(greek_value(c) for c in text),
        "pythagorean_sum":   sum(pythagorean_value(c) for c in text),
        "life_path":         life_path_number(text),
        "digital_root":      reduce(text),
    }
