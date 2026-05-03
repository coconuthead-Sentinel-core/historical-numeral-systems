"""
codex.py — unified API across all five traditions.

The functions here are the high-level "tools the AI assistant uses while coding."
Each one returns a small dict that summarizes a piece of input through one or
more lenses simultaneously.
"""
from __future__ import annotations
from datetime import datetime, timezone
from .traditions import gematria, isopsephy, abjad, vedic, metrology


def fingerprint(text: str) -> dict:
    """
    Run text through all five traditions at once.
    Returns a unified fingerprint useful for content tagging,
    deduplication keys, complexity scoring.
    """
    return {
        "text":         text,
        "gematria":     gematria.fingerprint(text),
        "isopsephy":    isopsephy.fingerprint(text),
        "abjad":        abjad.fingerprint(text),
        "vedic":        vedic.fingerprint(text),
    }


def glyph_id(prefix: str, subtype: str, content: str) -> str:
    """
    Generate a content-derived doc_id matching the NLCA pattern
    PREFIX-TYPE-NNN where NNN is the gematria digital root x 100 + Pythagorean
    digital root x 10 + Vedic life number, mod 1000.

    Compatible with the NLCA `^[A-Z]{3,4}-[A-Z]{3,6}-[0-9]{3}$` regex.
    """
    g = gematria.reduce(content)             # 1-9
    p = isopsephy.life_path_number(content)  # 1-9
    v = vedic.life_number(content)           # 0-9
    n = (g * 100 + p * 10 + v) % 1000
    return f"{prefix.upper()[:4]}-{subtype.upper()[:6]}-{n:03d}"


def complexity_score(text: str) -> dict:
    """
    Return a 1-10 cognitive complexity score for any text.
    Useful as a NLCA cognitive_load classifier.

    Heuristic:
      - syllable count (Vedic)
      - character count
      - gematria sum entropy
    """
    syl = vedic.syllable_count(text)
    chars = len(text)
    gem = gematria.sum_word(text)
    # Simple normalization to 1-10
    score = 1 + min(9, syl // 3 + chars // 50 + (gem % 7))
    return {
        "text":             text,
        "score_1_10":       score,
        "syllable_count":   syl,
        "char_count":       chars,
        "gematria_sum":     gem,
        "nlca_zone":        "GREEN" if score >= 7 else "YELLOW" if score >= 4 else "RED",
    }


def chronogram_year() -> int:
    """Return the current year as an abjad chronogram could encode it."""
    return datetime.now(timezone.utc).year


def encode_now_sexagesimal() -> dict:
    """The current UTC time encoded as a Mesopotamian time triple."""
    now = datetime.now(timezone.utc)
    seconds_today = now.hour * 3600 + now.minute * 60 + now.second
    return {
        "iso8601":           now.isoformat(),
        "seconds_into_day":  seconds_today,
        **metrology.fingerprint(seconds_today),
    }


def primer() -> str:
    """A brief reference card for the AI assistant's quick recall."""
    return """
ANCIENT NUMERICS CODEX — quick reference

5 TRADITIONS (each importable as ancient_numerics.traditions.<name>)
  gematria   Hebrew letter->int sums + reduction
  isopsephy  Greek/Pythagorean letter values + psephos
  abjad      Arabic letter values + chronograms
  vedic      Sanskrit-style syllable count + planetary numerology
  metrology  Mesopotamian base-60 (sexagesimal) for time/angles/fractions

3 PRIMITIVES (ancient_numerics.primitives.<name>)
  digital_root, weighted_sum, base_n

UNIFIED API (ancient_numerics.codex)
  fingerprint(text)           - run through all 5 traditions
  glyph_id(prefix, subtype,
          content)            - generate NLCA-compatible doc_id
  complexity_score(text)      - 1-10 cognitive load + NLCA zone
  encode_now_sexagesimal()    - current time in Babylonian form

USE FROM CODE:
  from ancient_numerics import codex
  print(codex.glyph_id('CSTM', 'EVENT', 'lattice intake'))
  -> e.g. 'CSTM-EVENT-413'
""".strip()
