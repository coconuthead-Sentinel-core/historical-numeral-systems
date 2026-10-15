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
