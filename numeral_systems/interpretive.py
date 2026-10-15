"""
interpretive.py -- practices that read MEANING from letter values.

The modules in ``numeral_systems.systems`` represent quantity. This module
is about something else: traditions that take the numeric value of a word
and treat the result as significant. The two activities use the same
arithmetic and are not the same subject, which is why they are kept apart
here. Claim key: ``notation-is-not-interpretation``.

WHAT IS DOCUMENTED HERE

``gematria`` -- Hebrew. Exegetical technique: comparing words whose letter
sums agree in order to draw a reading out of a text. Attested in late
antiquity and developed extensively in later Kabbalistic literature. It is
a method of INTERPRETATION applied to scripture, not a method of
calculation, and it was never a competing numeral system.

``isopsephy`` -- Greek. The same arithmetic applied to Greek: equal-psephos
words set against each other, used in wordplay, inscriptions and riddles.

``chronograms`` -- Arabic, Persian, Urdu. Treated separately in
``numeral_systems.chronograms``, because a chronogram records a VERIFIABLE
date. It is the one practice in this family with a checkable answer, which
puts it closer to notation than to interpretation.

WHAT IS NOT IMPLEMENTED HERE, AND WHY

Modern numerology -- life path numbers, name numbers, planetary
correspondences for the digits 1 to 9 -- is NOT implemented by this
library. It is described below so the omission is informed rather than
squeamish:

  * The name-and-birth-date method is early-20th-century and American,
    originating with L. Dow Balliett in the New Thought movement and
    formalised further by Juno Jordan. Claim key: ``life-path-is-modern``.
  * Its "Pythagorean" label is borrowed. The Pythagorean school did hold
    views about number and cosmic order, but the specific letter-to-number
    and digit-reduction method has no documented basis in anything that
    school wrote or practised. Claim key:
    ``pythagorean-label-is-borrowed``.
  * The planetary correspondences marketed as "Vedic numerology" are not
    supported in the scholarly record. No Vedic text sets them out, and the
    best scholarly description of the modern practice is a synthesis of
    jyotish planetary language, the Chinese Lo Shu grid, and Western
    name-number methods. This is a gap in the evidence, not a demonstrated
    forgery, and this library states it that way. Claim key:
    ``vedic-attribution-unsupported``.

An earlier version of this library implemented ``life_number``,
``destiny_number``, ``soul_number`` and planetary meanings, and described
them as classical and Vedic. Those functions were removed on verification.
The letter-sum arithmetic they rested on is still available, correctly
named, in the ``systems`` modules.
"""
from __future__ import annotations
from itertools import permutations

from .systems import hebrew, greek, arabic
from .primitives import digital_root

# Named so that a reader cannot mistake this module's subject matter.
IS_NOT_A_NUMERAL_SYSTEM = True

PRACTICES: dict[str, dict[str, str]] = {
    "gematria": {
        "language": "Hebrew",
        "period": "attested in late antiquity; developed in later Kabbalah",
        "activity": "exegesis -- comparing words of equal letter-sum",
        "verifiable": "no -- a reading, not a result",
        "claim": "notation-is-not-interpretation",
    },
    "isopsephy": {
        "language": "Greek",
        "period": "classical and later antiquity",
        "activity": "wordplay and riddle -- equal-psephos words",
        "verifiable": "no -- a reading, not a result",
        "claim": "notation-is-not-interpretation",
    },
    "chronogram": {
        "language": "Arabic, Persian, Urdu",
        "period": "letter values from the 12th century; organised phrases "
                  "from around the turn of the 14th",
        "activity": "recording a date inside a word or phrase",
        "verifiable": "yes -- the sum either equals the year or does not",
        "claim": "chronograms-attested",
    },
}


def letter_sum(text: str, script: str) -> int:
    """The letter-sum of ``text`` in one of the three scripts.

    ``script`` is 'hebrew', 'greek' or 'arabic'. This is the shared
    arithmetic underneath all three practices.
    """
    if script == "hebrew":
        return hebrew.letter_sum(text)
    if script == "greek":
        return greek.psephos(text)
    if script == "arabic":
        return arabic.letter_sum(text)
    raise ValueError(
        f"Unknown script {script!r}. Expected 'hebrew', 'greek' or 'arabic'."
    )


def reduce_to_root(text: str, script: str) -> int:
    """The digital root of a letter-sum.

    Digital root is ordinary number theory -- repeated digit-summing, which
    is congruence modulo 9 for any positive integer. Reducing a letter-sum
    this way is a MODERN numerological habit, not an ancient one; it is
    offered here as arithmetic, with no claim attached to the result.
    """
    return digital_root(letter_sum(text, script))


# Permutation count grows factorially, so the input is capped rather than
# left to the caller's optimism. 8! is 40320, which is cheap; 12! is not.
MAX_PERMUTED_LETTERS = 8


def equal_sum_variants(text: str, script: str, limit: int = 100) -> list[str]:
    """Rearrangements of ``text`` sharing its letter-sum. Stops at ``limit``.

    Every one of them, because a letter-sum is order-independent. This
    function exists to make that concrete: it is the reason a letter-sum
    cannot serve as a content fingerprint, and the reason this library does
    not derive identifiers from one.

    Raises ValueError for inputs longer than ``MAX_PERMUTED_LETTERS``
    scoring letters. Permutations grow factorially and a silent slowdown
    would be worse than a refusal that says why.
    """
    if limit < 1:
        raise ValueError(f"limit must be at least 1; got {limit}.")
    letters = [c for c in text if letter_sum(c, script) > 0]
    if len(letters) > MAX_PERMUTED_LETTERS:
        raise ValueError(
            f"{len(letters)} scoring letters would mean "
            f"{len(letters)}! permutations. This demonstration caps at "
            f"{MAX_PERMUTED_LETTERS}; pass a shorter word."
        )
    seen: set[str] = set()
    out: list[str] = []
    for perm in permutations(letters):
        candidate = "".join(perm)
        if candidate in seen:
            continue
        seen.add(candidate)
        out.append(candidate)
        if len(out) >= limit:
            break
    return out


def collision_demonstration(text: str, script: str) -> dict:
    """Show that a letter-sum identifies a multiset of letters, not a word.

    Returns the sum, how many distinct rearrangements were found sharing
    it, and a sample. Used in the classroom material and in the test suite.
    """
    variants = equal_sum_variants(text, script)
    total = letter_sum(text, script)
    return {
        "text": text,
        "script": script,
        "letter_sum": total,
        "collisions_found": len(variants),
        "sample": variants[:5],
        "all_share_the_sum": all(
            letter_sum(v, script) == total for v in variants
        ),
    }
