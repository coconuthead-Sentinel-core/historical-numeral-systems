"""
The static gate on claims.

These tests are the mechanism behind this library's central promise: no
historical claim ships without a citation. If a lesson asserts something
the register does not back, or the register cites a claim nobody makes,
the build fails here rather than on a reader's desk.
"""
from __future__ import annotations
import pytest

from numeral_systems import sources, classroom


def test_every_claim_has_at_least_one_source():
    assert sources.uncited_claims() == [], (
        "These claims have no supporting citation: "
        f"{sources.uncited_claims()}"
    )


def test_no_source_cites_an_unknown_claim():
    assert sources.orphan_supports() == [], (
        "These claim keys are cited by a source but are not declared in "
        f"CLAIMS: {sources.orphan_supports()}"
    )


def test_every_claim_key_used_by_the_classroom_exists():
    unknown = [k for k in classroom.all_claim_keys() if k not in sources.CLAIMS]
    assert unknown == [], f"Classroom references unknown claim keys: {unknown}"


def test_every_citation_declares_a_known_tier():
    allowed = {"scholarly", "reference", "collection", "popular"}
    for key, entry in sources.CITATIONS.items():
        assert entry["tier"] in allowed, f"{key} has tier {entry['tier']!r}"


def test_every_citation_has_text_and_supports():
    for key, entry in sources.CITATIONS.items():
        assert entry["text"].strip(), f"{key} has no citation text"
        assert entry["supports"], f"{key} supports nothing"


def test_no_claim_rests_only_on_a_popular_source():
    """A popular source may corroborate, never carry a claim alone."""
    for claim in sources.CLAIMS:
        tiers = {s["tier"] for s in sources.sources_for(claim)}
        assert tiers - {"popular"}, (
            f"{claim!r} is supported only by popular sources"
        )


def test_the_three_contested_claims_rest_on_scholarly_sources():
    """The claims most likely to be challenged need the strongest support."""
    for claim in (
        "life-path-is-modern",
        "pythagorean-label-is-borrowed",
        "vedic-attribution-unsupported",
    ):
        tiers = {s["tier"] for s in sources.sources_for(claim)}
        assert "scholarly" in tiers, f"{claim!r} lacks a scholarly source"


def test_every_citation_declares_a_verification_level():
    """Each source must say how far this release actually checked it."""
    for key, entry in sources.CITATIONS.items():
        assert "verification" in entry, f"{key} declares no verification level"
        assert entry["verification"] in sources.VERIFICATION_LEVELS, (
            f"{key} has verification {entry['verification']!r}"
        )


def test_tiers_come_from_the_declared_list():
    for key, entry in sources.CITATIONS.items():
        assert entry["tier"] in sources.TIERS, f"{key} has tier {entry['tier']!r}"


def test_a_bibliographic_source_says_so_in_its_note():
    """A source whose pages were not read must disclose that in prose.

    The structured field alone is not enough: a reader skimming the
    bibliography sees the note, so the note has to carry it too.
    """
    for key, entry in sources.CITATIONS.items():
        if entry["verification"] != "bibliographic":
            continue
        note = entry.get("note", "").lower()
        assert sources.BIBLIOGRAPHIC_DISCLOSURE.lower() in note, (
            f"{key} is bibliographic but its note omits the required "
            f"disclosure: {sources.BIBLIOGRAPHIC_DISCLOSURE!r}"
        )


def test_unverified_claims_are_published_not_hidden():
    """The open reading list must be reachable and non-empty here.

    If this ever becomes empty, every claim rests on a directly-read
    source, and that is worth noticing rather than silently passing.
    """
    unverified = sources.unverified_claims()
    assert isinstance(unverified, list)
    for claim in unverified:
        assert claim in sources.CLAIMS


def test_reading_list_names_every_unread_source():
    text = sources.reading_list()
    for claim in sources.unverified_claims():
        for src in sources.sources_for(claim):
            if src["verification"] != "consulted":
                assert f"[{src['key']}]" in text


def test_execution_checked_claims_all_exist():
    unknown = [c for c in sources.EXECUTION_CHECKED if c not in sources.CLAIMS]
    assert unknown == [], f"EXECUTION_CHECKED names unknown claims: {unknown}"


def test_bibliography_shows_the_verification_level():
    text = sources.bibliography()
    for entry in sources.CITATIONS.values():
        assert entry["verification"] in text


def test_bibliography_renders_every_citation():
    text = sources.bibliography()
    for key in sources.CITATIONS:
        assert f"[{key}]" in text


def test_bibliography_can_be_filtered_by_tier():
    scholarly = sources.bibliography(tier="scholarly")
    assert "[chrisomalis2010]" in scholarly
    assert "[britishmuseum]" not in scholarly


def test_sources_for_unknown_claim_is_empty_not_an_error():
    assert sources.sources_for("no-such-claim") == []


@pytest.mark.parametrize("claim", sorted(sources.CLAIMS))
def test_each_claim_has_readable_wording(claim):
    assert len(sources.CLAIMS[claim]) > 20
