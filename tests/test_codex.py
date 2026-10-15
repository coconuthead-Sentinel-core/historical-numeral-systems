"""
Tests for the unified API, readability, the interpretive module and
chronograms.

Several of these are regression guards against defects found in v0.1.0 and
are labelled as such.
"""
from __future__ import annotations
import pytest

from numeral_systems import codex, readability, interpretive, chronograms
from numeral_systems.systems import greek, arabic


# ----------------------------------------------------------- letter_sums

def test_letter_sums_reports_all_three_scripts():
    result = codex.letter_sums("αβ")
    assert set(result) == {"text", "hebrew", "greek", "arabic"}


def test_letter_sums_counts_only_the_matching_script():
    result = codex.letter_sums("αβγ")
    assert result["greek"] == 6
    assert result["hebrew"] == 0
    assert result["arabic"] == 0


def test_letter_sums_of_latin_text_is_zero_everywhere():
    """v0.1.0 invented Latin transliteration tables. They were removed."""
    result = codex.letter_sums("hello world")
    assert result["hebrew"] == 0
    assert result["greek"] == 0
    assert result["arabic"] == 0


# -------------------------------------------------------------- glyph_id

def test_glyph_id_matches_the_required_pattern():
    import re
    pattern = re.compile(r"^[A-Z]{3,4}-[A-Z]{3,6}-[0-9]{3}$")
    assert pattern.match(codex.glyph_id("CSTM", "EVENT", "lattice intake"))


def test_glyph_id_is_deterministic():
    a = codex.glyph_id("CSTM", "EVENT", "lattice intake")
    b = codex.glyph_id("CSTM", "EVENT", "lattice intake")
    assert a == b


def test_glyph_id_is_order_sensitive():
    """The regression guard. v0.1.0 used letter-sums, so anagrams collided."""
    a = codex.glyph_id("DOC", "NOTE", "abc")
    b = codex.glyph_id("DOC", "NOTE", "cba")
    assert a != b


def test_glyph_id_truncates_long_prefixes():
    assert codex.glyph_id("TOOLONG", "SUBTYPELONG", "x").startswith("TOOL-")


def test_glyph_id_requires_content():
    with pytest.raises(ValueError, match="non-empty"):
        codex.glyph_id("DOC", "NOTE", "")


def test_glyph_id_tail_stays_inside_the_id_space():
    for i in range(200):
        tail = int(codex.glyph_id("DOC", "NOTE", f"content {i}").split("-")[-1])
        assert 0 <= tail < codex.ID_SPACE


def test_collision_probability_is_honest_about_the_birthday_bound():
    """Three digits is 1000 buckets: a coin flip at about 38 documents."""
    assert codex.collision_probability(1) == 0.0
    assert codex.collision_probability(38) > 0.5
    assert codex.collision_probability(37) < codex.collision_probability(38)
    assert codex.collision_probability(codex.ID_SPACE + 1) == 1.0


def test_collision_probability_rejects_negatives():
    with pytest.raises(ValueError):
        codex.collision_probability(-1)


# ----------------------------------------------------------- readability

def test_readability_band_is_not_inverted():
    """The regression guard for the v0.1.0 inversion.

    v0.1.0 returned GREEN -- its most permissive label -- for its most
    complex input. Harder text must now give a harder band.
    """
    easy = "The cat sat. The dog ran. It was fun."
    hard = (
        "Notwithstanding the aforementioned considerations, the "
        "institutional ramifications of epistemological relativism "
        "necessitate comprehensive reconceptualization."
    )
    easy_grade = readability.flesch_kincaid_grade(easy)
    hard_grade = readability.flesch_kincaid_grade(hard)
    assert hard_grade > easy_grade
    assert readability.difficulty_band(easy) == "EASY"
    assert readability.difficulty_band(hard) == "HARD"


def test_readability_is_deterministic():
    """v0.1.0 added the gematria sum modulo 7, an arbitrary 0-6 swing."""
    text = "A sentence with several syllables in it."
    assert readability.report(text) == readability.report(text)


def test_texts_of_equal_shape_score_equally():
    """The noise term made same-shaped texts score differently."""
    a = "The cat sat on the mat."
    b = "The dog ran in the fog."
    assert readability.syllable_count(a) == readability.syllable_count(b)
    assert readability.flesch_kincaid_grade(a) == readability.flesch_kincaid_grade(b)


def test_readability_returns_none_for_empty_text():
    assert readability.flesch_reading_ease("") is None
    assert readability.flesch_kincaid_grade("") is None
    assert readability.difficulty_band("") is None


def test_sentence_count_never_divides_by_zero():
    assert readability.sentence_count("no terminal punctuation here") == 1
    assert readability.sentence_count("") == 0


def test_syllable_count_basic_cases():
    assert readability.syllable_count("cat") == 1
    assert readability.syllable_count("beautiful") == 3
    assert readability.syllable_count("") == 0


def test_codex_readability_delegates():
    assert codex.readability("A short sentence.") == readability.report(
        "A short sentence."
    )


# ---------------------------------------------------------- interpretive

def test_interpretive_declares_it_is_not_a_numeral_system():
    assert interpretive.IS_NOT_A_NUMERAL_SYSTEM is True


def test_interpretive_does_not_expose_removed_numerology():
    for removed in (
        "life_number", "life_path_number", "soul_number",
        "destiny_number", "number_meaning",
    ):
        assert not hasattr(interpretive, removed), (
            f"{removed} was retired on verification and must not return"
        )


def test_only_the_chronogram_practice_is_marked_verifiable():
    verifiable = {
        name for name, p in interpretive.PRACTICES.items()
        if p["verifiable"].startswith("yes")
    }
    assert verifiable == {"chronogram"}


def test_letter_sum_dispatches_by_script():
    assert interpretive.letter_sum("αβγ", "greek") == 6


def test_letter_sum_rejects_an_unknown_script():
    with pytest.raises(ValueError, match="Unknown script"):
        interpretive.letter_sum("abc", "latin")


def test_collision_demonstration_proves_order_independence():
    word = greek.to_greek(123)
    demo = interpretive.collision_demonstration(word, "greek")
    assert demo["all_share_the_sum"] is True
    assert demo["collisions_found"] > 1


# ----------------------------------------------------------- chronograms

def test_chronogram_verify_matches_an_exact_sum():
    word = arabic.to_abjad(1121)
    result = chronograms.verify(word, 1121)
    assert result["matches"] is True
    assert result["delta"] == 0


def test_chronogram_reports_a_signed_delta_on_a_miss():
    word = arabic.to_abjad(1121)
    result = chronograms.verify(word, 1120)
    assert result["matches"] is False
    assert result["delta"] == 1


def test_chronogram_records_which_abjad_order_was_used():
    assert chronograms.verify(arabic.to_abjad(5), 5)["order"] == "eastern"


def test_chronogram_candidates_filters_a_wordlist():
    wordlist = [arabic.to_abjad(469), arabic.to_abjad(470)]
    assert chronograms.candidates(wordlist, 469) == [wordlist[0]]


def test_chronogram_ships_no_lexicon():
    assert chronograms.candidates([], 1443) == []


def test_compose_hint_round_trips_its_own_skeleton():
    hint = chronograms.compose_hint(469)
    assert hint["checks_back_to"] == 469
    assert sum(hint["letter_values"]) == 469


def test_approximate_ce_is_in_the_right_region():
    """469 AH falls in the late 11th century CE."""
    assert 1070 <= chronograms.approximate_ce(469) <= 1085


def test_approximate_ce_rejects_year_zero():
    with pytest.raises(ValueError, match="start at 1"):
        chronograms.approximate_ce(0)


# ------------------------------------------------------------------ misc

def test_primer_names_what_is_not_implemented():
    text = codex.primer()
    assert "NOT IMPLEMENTED" in text
    assert "life path" in text


def test_bibliography_is_reachable_from_the_codex():
    assert "chrisomalis2010" in codex.bibliography()


def test_encode_now_sexagesimal_reports_a_wedge_layout():
    result = codex.encode_now_sexagesimal()
    assert "wedge_layout" in result
    assert "iso8601" in result


def test_codex_no_longer_exposes_the_retired_functions():
    for removed in ("fingerprint", "complexity_score", "chronogram_year"):
        assert not hasattr(codex, removed), (
            f"{removed} was retired and must not return"
        )
