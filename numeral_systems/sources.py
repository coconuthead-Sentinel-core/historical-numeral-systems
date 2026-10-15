"""
sources.py -- the citation register for this library.

Every historical claim made anywhere in this package cites a key from
``CITATIONS`` below. ``tests/test_sources.py`` enforces that: a claim with
no citation key, or a key with no entry here, fails the build. This is the
mechanism, not the promise -- an uncited claim cannot ship.

TWO AXES, DELIBERATELY SEPARATE

``tier`` says what KIND of source it is:

    "scholarly"  peer-reviewed or university-press monograph
    "reference"  specialist encyclopaedia or standards body
    "collection" a museum or national library holding primary material
    "popular"    general-audience source; may corroborate, never carry a
                 claim alone

``verification`` says HOW FAR THIS RELEASE ACTUALLY CHECKED IT:

    "consulted"     the source text was read directly while preparing
                    this release
    "bibliographic" the citation's details were confirmed and the source
                    is the recognised authority for the claim, but its
                    pages were NOT read while preparing this release
    "reported"      known here only through secondary summaries

Most entries below are "bibliographic". That is stated rather than
implied, because a citation can be correct and still be a claim about
one's own diligence. A reader who wants page-level confirmation has the
exact editions to check, and ``unverified_claims()`` lists every claim
that no directly-read source supports.

This is the honest position for a library assembled without a research
library at hand. It is not a substitute for reading the books, and the
register says which books still want reading.

Citation style throughout: Chicago notes-bibliography, author-first.
"""
from __future__ import annotations

VERIFICATION_LEVELS = ("consulted", "bibliographic", "reported")

# Every "bibliographic" entry must repeat this sentence in its note, so a
# reader skimming the bibliography sees the limitation and not only the
# structured field. Enforced by tests/test_sources.py.
BIBLIOGRAPHIC_DISCLOSURE = "Not directly examined for this release."
TIERS = ("scholarly", "reference", "collection", "popular")


CITATIONS: dict[str, dict] = {
    # ------------------------------------------------------------------
    # Comparative numerical notation -- the spine of this library
    # ------------------------------------------------------------------
    "chrisomalis2010": {
        "tier": "scholarly",
        "verification": "bibliographic",
        "text": (
            "Chrisomalis, Stephen. Numerical Notation: A Comparative "
            "History. Cambridge: Cambridge University Press, 2010. "
            "ISBN 978-0-521-87818-0."
        ),
        "note": (
            "Surveys more than 100 attested numerical notation systems "
            "across roughly 5,500 years. Originated as the author's PhD "
            "thesis at McGill University; the author is at Wayne State "
            "University. This is the standard comparative reference for "
            "every system in this package. Not directly examined for this "
            "release. The structural claims it is cited for are the ones a "
            "reader should check against it first."
        ),
        "supports": [
            "alphabetic-numerals-are-numeral-systems",
            "greek-milesian-structure",
            "hebrew-from-greek",
            "abjad-decimal-structure",
            "sexagesimal-positional",
        ],
    },
    "chrisomalis2021": {
        "tier": "scholarly",
        "verification": "bibliographic",
        "text": (
            "Chrisomalis, Stephen. Reckonings: Numerals, Cognition, and "
            "History. Cambridge, MA: MIT Press, 2021."
        ),
        "note": (
            "Cognitive and historical analysis of numeral systems. "
            "Not directly examined for this release."
        ),
        "supports": ["notation-is-not-interpretation"],
    },
    # ------------------------------------------------------------------
    # The critical literature on numerology
    # ------------------------------------------------------------------
    "dudley1997": {
        "tier": "scholarly",
        "verification": "bibliographic",
        "text": (
            "Dudley, Underwood. Numerology: Or, What Pythagoras Wrought. "
            "Washington, DC: Mathematical Association of America, 1997."
        ),
        "note": (
            "A mathematician's history and critique of numerology, and "
            "the standard academic treatment. Cited for the finding that "
            "the modern name-and-birth-date method has no documented "
            "basis in the Pythagorean school, and for L. Dow Balliett's "
            "role in originating it. Not directly examined for this release."
        ),
        "supports": [
            "life-path-is-modern",
            "pythagorean-label-is-borrowed",
            "notation-is-not-interpretation",
        ],
    },
    # ------------------------------------------------------------------
    # South Asian mathematics -- for what the record does and does not say
    # ------------------------------------------------------------------
    "plofker2009": {
        "tier": "scholarly",
        "verification": "bibliographic",
        "text": (
            "Plofker, Kim. Mathematics in India. Princeton: Princeton "
            "University Press, 2009."
        ),
        "note": (
            "The standard history of Indian mathematics. Cited here for "
            "the documented record of Indian numeration, and as the "
            "scholarly counterweight to systems marketed as 'Vedic' "
            "whose content does not appear in the Vedic corpus. Not "
            "directly examined for this release."
        ),
        "supports": ["vedic-attribution-unsupported"],
    },
    "murthy2005": {
        "tier": "scholarly",
        "verification": "reported",
        "text": (
            "Murthy, S. S. N. 'Number Symbolism in the Vedas.' Electronic "
            "Journal of Vedic Studies 12, no. 3 (2005)."
        ),
        "note": (
            "Examines number symbolism in the Vedic corpus. Reported to "
            "state that the extent of Vedic influence on modern "
            "numerology is not known -- a gap in the record, which is why "
            "this library treats the 'Vedic numerology' label as "
            "unsupported rather than as disproven. Known here through "
            "secondary summary; the article is open access and should be "
            "read directly before the claim is strengthened."
        ),
        "supports": ["vedic-attribution-unsupported"],
    },
    # ------------------------------------------------------------------
    # Chronograms
    # ------------------------------------------------------------------
    "iranica-chronograms": {
        "tier": "reference",
        "verification": "reported",
        "text": (
            "'Chronograms' (madda tarikh). Encyclopaedia Iranica. "
            "https://www.iranicaonline.org/"
        ),
        "note": (
            "Documents the Persian chronogram tradition: early poets "
            "wrote years out in words; later poets used abjad letter "
            "values, and from around the turn of the 14th century "
            "organised those values into meaningful words and phrases, a "
            "technique called hisab al-jummal. Mas'ud-e Sa'd-e Salman "
            "(d. 1121) is an attested early example, encoding 469 AH. "
            "Known here through secondary summary of the entry."
        ),
        "supports": ["chronograms-attested", "chronogram-phrase-era"],
    },
    # ------------------------------------------------------------------
    # Readability -- the one quantitative claim this library makes about text
    # ------------------------------------------------------------------
    "flesch1948": {
        "tier": "scholarly",
        "verification": "bibliographic",
        "text": (
            "Flesch, Rudolf. 'A New Readability Yardstick.' Journal of "
            "Applied Psychology 32, no. 3 (1948): 221-33."
        ),
        "note": (
            "Origin of the Reading Ease formula implemented here. The "
            "formula's coefficients are long-standardised and were taken "
            "from the standard statement of it. Not directly examined for "
            "this release."
        ),
        "supports": ["readability-formulas-are-published"],
    },
    "kincaid1975": {
        "tier": "scholarly",
        "verification": "bibliographic",
        "text": (
            "Kincaid, J. Peter, Robert P. Fishburne, Richard L. Rogers "
            "and Brad S. Chissom. 'Derivation of New Readability Formulas "
            "for Navy Enlisted Personnel.' Naval Technical Training "
            "Command, Research Branch Report 8-75, 1975."
        ),
        "note": (
            "Origin of the Flesch-Kincaid Grade Level formula, likewise "
            "taken from its standard statement. Not directly examined for "
            "this release."
        ),
        "supports": ["readability-formulas-are-published"],
    },
    # ------------------------------------------------------------------
    # Standards
    # ------------------------------------------------------------------
    "unicode": {
        "tier": "reference",
        "verification": "consulted",
        "text": (
            "The Unicode Standard. Unicode Consortium. "
            "https://www.unicode.org/versions/latest/"
        ),
        "note": (
            "Normative source for the code points of the three Greek "
            "numeral-only letters -- stigma (U+03DB), koppa (U+03DF) and "
            "sampi (U+03E1) -- and of their archaic alphabetic forms. "
            "Every code point this library hard-codes round-trips in the "
            "test suite, so the assignment is checked by execution as "
            "well as by citation."
        ),
        "supports": ["greek-milesian-structure", "greek-obsolete-letters"],
    },
    # ------------------------------------------------------------------
    # Collections holding the primary material
    # ------------------------------------------------------------------
    "britishmuseum": {
        "tier": "collection",
        "verification": "bibliographic",
        "text": "The British Museum, London. Mesopotamian collection.",
        "note": (
            "Holds cuneiform mathematical tablets. Following the "
            "mid-19th-century Mesopotamian excavations, the bulk of this "
            "material came to rest in the British Museum, the Louvre and "
            "Berlin, and in university collections. No object numbers "
            "are asserted here; the collection databases are the place "
            "to cite specific tablets. Not directly examined for "
            "this release."
        ),
        "supports": ["sexagesimal-primary-material"],
    },
    "louvre": {
        "tier": "collection",
        "verification": "bibliographic",
        "text": "Musee du Louvre, Paris. Near Eastern Antiquities.",
        "note": (
            "Holds Mesopotamian primary material, including tablets. "
            "Not directly examined for this release."
        ),
        "supports": ["sexagesimal-primary-material"],
    },
    "vorderasiatisches": {
        "tier": "collection",
        "verification": "bibliographic",
        "text": (
            "Vorderasiatisches Museum (Pergamonmuseum), Staatliche "
            "Museen zu Berlin."
        ),
        "note": (
            "Holds one of the major cuneiform collections. Not "
            "directly examined for this release."
        ),
        "supports": ["sexagesimal-primary-material"],
    },
}


# Claims this library makes, each mapped to the keys that support it.
# A claim listed here with an empty source list is a build failure.
CLAIMS: dict[str, str] = {
    "alphabetic-numerals-are-numeral-systems": (
        "Hebrew, Greek and Arabic letters were used as numerals for "
        "ordinary counting and dating. These are numeral systems."
    ),
    "greek-milesian-structure": (
        "The Greek Milesian system is additive and decimal: nine units, "
        "nine tens, nine hundreds, for 27 values in all."
    ),
    "greek-obsolete-letters": (
        "Because the Greek alphabet has 24 letters and the system needs "
        "27 values, three letters outside the classical alphabet carry "
        "6, 90 and 900: stigma, koppa and sampi."
    ),
    "hebrew-from-greek": (
        "The Hebrew alphabetic numerals were adapted from the Greek "
        "system; with 22 letters the series stops at 400."
    ),
    "abjad-decimal-structure": (
        "The Arabic abjad numerals match the Hebrew values up to 400; "
        "the additional Arabic letters carry 500 through 1000."
    ),
    "sexagesimal-positional": (
        "Mesopotamian notation is positional, base 60, with a sub-base "
        "of 10 inside each digit, and no true zero sign."
    ),
    "sexagesimal-primary-material": (
        "The primary cuneiform material is held chiefly in the British "
        "Museum, the Louvre and Berlin."
    ),
    "chronograms-attested": (
        "Encoding a date in the abjad values of a word or phrase is an "
        "attested historical practice in Persian and Urdu literature."
    ),
    "chronogram-phrase-era": (
        "Organising abjad values into meaningful phrases dates from "
        "around the turn of the 14th century."
    ),
    "life-path-is-modern": (
        "The name-and-birth-date 'life path' method is early-20th-century "
        "and American, originating with L. Dow Balliett."
    ),
    "pythagorean-label-is-borrowed": (
        "The 'Pythagorean' label on modern numerology is borrowed. The "
        "method has no documented basis in the Pythagorean school."
    ),
    "vedic-attribution-unsupported": (
        "The 'Vedic' attribution for planetary numerology is unsupported "
        "in the scholarly record. This is a gap in the evidence, not a "
        "demonstrated forgery."
    ),
    "notation-is-not-interpretation": (
        "Representing quantity (numerical notation) and extracting "
        "meaning from letter values (gematria, isopsephy, numerology) "
        "are different activities and belong in different modules."
    ),
    "readability-formulas-are-published": (
        "Reading difficulty can be estimated by published formulas with "
        "named authors and dates. Readability is not cognitive load."
    ),
}

# Claims the code additionally proves by execution, independent of any
# citation. Named here so the distinction is explicit: a test can confirm
# that a table is internally consistent and round-trips, which is not the
# same as confirming it matches the historical record.
EXECUTION_CHECKED: dict[str, str] = {
    "greek-obsolete-letters": (
        "tests/test_systems.py round-trips 6, 90, 900 and 96 through the "
        "encoder and decoder, so the code-point assignments are checked "
        "by execution as well as by citation."
    ),
    "sexagesimal-positional": (
        "tests/test_systems.py verifies every digit 0-59 decomposes into "
        "at most five tens wedges and nine units wedges and recomposes "
        "exactly, so the sub-base claim is checked by execution."
    ),
    "readability-formulas-are-published": (
        "tests/test_codex.py verifies the formulas are deterministic and "
        "monotone in difficulty."
    ),
}


def sources_for(claim: str) -> list[dict]:
    """Every citation supporting ``claim``, in register order.

    Returns an empty list for an unknown claim; callers that require a
    citation should treat that as an error rather than a silence.
    """
    return [
        dict(key=key, **entry)
        for key, entry in CITATIONS.items()
        if claim in entry["supports"]
    ]


def uncited_claims() -> list[str]:
    """Claim keys with no supporting citation. Must be empty."""
    return sorted(c for c in CLAIMS if not sources_for(c))


def orphan_supports() -> list[str]:
    """Claim keys cited by a source but absent from ``CLAIMS``. Must be empty."""
    referenced: set[str] = set()
    for entry in CITATIONS.values():
        referenced.update(entry["supports"])
    return sorted(referenced - set(CLAIMS))


def unverified_claims() -> list[str]:
    """Claims no directly-read source supports.

    These are NOT errors. They are the library's open reading list: each
    rests on a recognised authority whose pages were not read while
    preparing this release. Published deliberately rather than hidden.
    """
    out = []
    for claim in CLAIMS:
        levels = {s["verification"] for s in sources_for(claim)}
        if "consulted" not in levels:
            out.append(claim)
    return sorted(out)


def reading_list() -> str:
    """The sources that would upgrade a claim from cited to read."""
    wanted: dict[str, list[str]] = {}
    for claim in unverified_claims():
        for src in sources_for(claim):
            if src["verification"] != "consulted":
                wanted.setdefault(src["key"], []).append(claim)
    lines = ["Sources not read while preparing this release:", ""]
    for key, claims in sorted(wanted.items()):
        lines.append(f"[{key}] {CITATIONS[key]['text']}")
        lines.append(f"    verification: {CITATIONS[key]['verification']}")
        for claim in sorted(claims):
            lines.append(f"    - would confirm: {claim}")
        lines.append("")
    return "\n".join(lines).rstrip()


def bibliography(tier: str | None = None) -> str:
    """The register as a readable block, optionally filtered by tier."""
    lines: list[str] = []
    for key, entry in sorted(CITATIONS.items()):
        if tier is not None and entry["tier"] != tier:
            continue
        lines.append(
            f"[{key}] ({entry['tier']}; {entry['verification']})"
        )
        lines.append(f"    {entry['text']}")
        if entry.get("note"):
            lines.append(f"    {entry['note']}")
        lines.append("")
    return "\n".join(lines).rstrip()
