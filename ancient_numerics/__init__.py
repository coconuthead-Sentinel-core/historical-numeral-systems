"""
Ancient Numerics Codex — five primordial mathematical traditions
brought to 2026 AI-tooling standards as composable Python primitives.

Traditions:
  - Hebrew Gematria         (gematria)
  - Greek Isopsephy / Pythagorean (isopsephy)
  - Arabic Abjad            (abjad)
  - Indian/Vedic numerology (vedic)
  - Mesopotamian metrology  (metrology, base-60 sexagesimal)

Primitives (used across traditions):
  - digital_root            (iterative sum-of-digits collapse)
  - weighted_sum            (positional weighted addition)
  - base_n                  (alternate-base arithmetic)

Public API:
    from ancient_numerics import codex
    codex.fingerprint("hello world")
    codex.glyph_id("CSTM-LATTICE-001")
    codex.complexity_score("a sentence with several syllables")
"""
__version__ = "0.1.0"

from . import codex
from . import classroom
from .traditions import gematria, isopsephy, abjad, vedic, metrology
from .primitives import digital_root, weighted_sum, base_n

__all__ = [
    "codex", "classroom",
    "gematria", "isopsephy", "abjad", "vedic", "metrology",
    "digital_root", "weighted_sum", "base_n",
]
