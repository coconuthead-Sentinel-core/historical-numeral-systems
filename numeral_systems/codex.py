"""
codex.py -- the unified API across this library.

Each function returns a small dict summarising its input. Nothing here
invents a claim the modules underneath do not support.

WHAT CHANGED FROM v0.1.0, and why, since the old names were published:

``glyph_id`` no longer derives an identifier from letter-sums. It used the
digital roots of a gematria sum, a mod-9 'Pythagorean' sum and a
'Vedic life number'. Two of those three had no documented basis, and all
three were order-independent, so anagrams collided by construction. It now
uses a real hash and states its own collision bound.

``complexity_score`` is gone, replaced by ``readability``. The old version
returned GREEN for its most complex input and RED for its simplest -- the
bands were inverted -- and it added the gematria sum modulo 7 to the score,
which put an arbitrary swing of 0 to 6 on a 1-to-10 scale.

``chronogram_year`` is gone. It returned the current calendar year and did
nothing with abjad values at all. ``numeral_systems.chronograms`` does the
real work.

``fingerprint`` is now ``letter_sums``, which is what it computes.
"""
from __future__ import annotations
import hashlib
from datetime import datetime, timezone

from . import readability as _readability
from . import sources
from .systems import hebrew, greek, arabic, sexagesimal

# glyph_id emits three decimal digits, so the identifier space is this big.
ID_SPACE = 1000


def letter_sums(text: str) -> dict:
    """The letter-sum of ``text`` in each of the three alphabetic systems.

    Each sum counts only the characters belonging to that script, so a
    Latin string returns zeros throughout. That is correct: these are
    numeral systems for their own scripts, and the earlier version's
    Latin transliteration tables were an invention with no source behind
    them.
    """
    return {
        "text": text,
        "hebrew": hebrew.letter_sum(text),
        "greek": greek.psephos(text),
        "arabic": arabic.letter_sum(text),
    }


def glyph_id(prefix: str, subtype: str, content: str) -> str:
    """A content-derived identifier matching ``[A-Z]{3,4}-[A-Z]{3,6}-[0-9]{3}``.

    The numeric tail is BLAKE2b over the content, reduced to three decimal
    digits. It is deterministic and order-SENSITIVE, which the previous
    letter-sum version was not.

    COLLISIONS ARE EXPECTED. Three digits give 1000 possible tails, so by
    the birthday bound there is roughly a even chance of a collision once
    about 38 documents share a prefix and subtype. Use
    ``collision_probability`` before treating one of these as a key. If you
    need uniqueness, widen the tail or add a check against what already
    exists -- this function cannot give you uniqueness and does not claim to.
    """
    if not content:
        raise ValueError("glyph_id requires non-empty content to hash.")
    digest = hashlib.blake2b(content.encode("utf-8"), digest_size=8).digest()
    tail = int.from_bytes(digest, "big") % ID_SPACE
    return f"{prefix.upper()[:4]}-{subtype.upper()[:6]}-{tail:03d}"


def collision_probability(n_documents: int) -> float:
    """Chance that ``n_documents`` ids collide, by the birthday bound.

    Returns a probability in 0.0 to 1.0, rounded to four places.
    """
    if n_documents < 0:
        raise ValueError("n_documents must be non-negative.")
    if n_documents > ID_SPACE:
        return 1.0
    probability_distinct = 1.0
    for i in range(n_documents):
        probability_distinct *= (ID_SPACE - i) / ID_SPACE
    return round(1.0 - probability_distinct, 4)


def readability(text: str) -> dict:
    """Published readability measures for ``text``.

    Delegates to ``numeral_systems.readability``. Higher grade means harder,
    and the band is oriented to match.
    """
    return _readability.report(text)


def encode_now_sexagesimal() -> dict:
    """The current UTC time rendered in sexagesimal places."""
    now = datetime.now(timezone.utc)
    seconds_today = now.hour * 3600 + now.minute * 60 + now.second
    return {
        "iso8601": now.isoformat(),
        "seconds_into_day": seconds_today,
        **sexagesimal.fingerprint(seconds_today),
    }


def primer() -> str:
    """A short reference card for this library."""
    return """
HISTORICAL NUMERAL SYSTEMS -- quick reference

NUMERAL SYSTEMS (numeral_systems.systems.<name>)
  hebrew        additive decimal, alphabetic; 1-400, adapted from Greek
  greek         additive decimal, alphabetic; 27 values incl. stigma,
                koppa, sampi
  arabic        additive decimal, alphabetic; eastern (mashriqi) abjad
  sexagesimal   POSITIONAL base 60 with sub-base 10; no zero sign

Each offers value(), an encoder, a decoder, and a letter-sum.

PRIMITIVES (numeral_systems.primitives.<name>)
  digital_root, weighted_sum, base_n

OTHER MODULES
  chronograms   recording a date inside a word (verifiable)
  interpretive  gematria, isopsephy -- documented, NOT computed as fact
  readability   Flesch and Flesch-Kincaid; syllable counting
  sources       the citation register; every claim keys into it

UNIFIED API (numeral_systems.codex)
  letter_sums(text)              sums in all three alphabetic systems
  glyph_id(prefix, subtype,
           content)              hashed id; see its collision bound
  collision_probability(n)       birthday bound for those ids
  readability(text)              Flesch / Flesch-Kincaid / band
  encode_now_sexagesimal()       current time in sexagesimal places

NOT IMPLEMENTED, DELIBERATELY
  life path, name, soul, destiny and planetary numbers. Early-20th-century
  numerology, not ancient notation. See numeral_systems.interpretive for
  the dating and the citations.
""".strip()


def bibliography() -> str:
    """Every source backing this library's claims."""
    return sources.bibliography()
