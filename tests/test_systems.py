"""
Tests for the four numeral systems.

The Greek block is the important one. The published v0.1.0 omitted stigma,
koppa and sampi, which made 6, 90, 900 and every number containing them
unrepresentable. These tests exist so that cannot regress.
"""
from __future__ import annotations
import pytest

from numeral_systems.systems import hebrew, greek, arabic, sexagesimal


# ---------------------------------------------------------------- Greek

def test_greek_table_has_all_twenty_seven_values():
    assert len(greek.UNITS) == 9
    assert len(greek.TENS) == 9
    assert len(greek.HUNDREDS) == 9


@pytest.mark.parametrize("n", [6, 90, 900])
def test_greek_represents_the_three_values_the_old_table_dropped(n):
    """The regression guard. These were unrepresentable in v0.1.0."""
    assert greek.from_greek(greek.to_greek(n)) == n


def test_greek_six_is_stigma():
    assert greek.to_greek(6) == greek.STIGMA


def test_greek_ninety_is_koppa():
    assert greek.to_greek(90) == greek.KOPPA


def test_greek_nine_hundred_is_sampi():
    assert greek.to_greek(900) == greek.SAMPI


def test_greek_accepts_digamma_as_six():
    assert greek.value(greek.DIGAMMA) == 6


def test_greek_accepts_archaic_variants():
    assert greek.value(greek.ARCHAIC_KOPPA) == 90
    assert greek.value(greek.ARCHAIC_SAMPI) == 900


def test_greek_ninety_six_round_trips():
    """96 needs both koppa and stigma -- impossible in v0.1.0."""
    assert greek.from_greek(greek.to_greek(96)) == 96


def test_greek_classic_example_two_four_one():
    assert greek.to_greek(241) == "σμα"


def test_greek_final_sigma_is_two_hundred():
    assert greek.value("ς") == 200


def test_greek_thousands_use_the_lower_numeral_sign():
    written = greek.to_greek(1998)
    assert written.startswith(greek.LOWER_KERAIA)
    assert greek.from_greek(written) == 1998


@pytest.mark.parametrize("n", list(range(1, 1000, 7)) + [1, 999, 9999])
def test_greek_round_trips_across_its_range(n):
    assert greek.from_greek(greek.to_greek(n)) == n


def test_greek_rejects_zero_and_negatives():
    with pytest.raises(ValueError, match="no zero"):
        greek.to_greek(0)
    with pytest.raises(ValueError):
        greek.to_greek(-5)


def test_greek_rejects_out_of_range_with_an_honest_message():
    with pytest.raises(ValueError, match="myriad"):
        greek.to_greek(10_000)


def test_greek_names_the_character_it_cannot_read():
    with pytest.raises(ValueError, match="carries no Milesian value"):
        greek.from_greek("z")


def test_greek_psephos_is_order_independent():
    assert greek.psephos("αβγ") == greek.psephos("γβα")


# --------------------------------------------------------------- Hebrew

def test_hebrew_table_stops_at_four_hundred():
    assert max(hebrew.HUNDREDS) == 4
    assert hebrew.VALUES[hebrew.HUNDREDS[4]] == 400


def test_hebrew_final_forms_match_their_ordinary_forms():
    for final, expected in hebrew.FINAL_FORMS.items():
        assert hebrew.value(final) == expected


def test_hebrew_fifteen_avoids_the_divine_name():
    """15 is tet-vav, not yod-he."""
    assert hebrew.to_hebrew(15) == hebrew.UNITS[9] + hebrew.UNITS[6]
    assert hebrew.from_hebrew(hebrew.to_hebrew(15)) == 15


def test_hebrew_sixteen_avoids_the_divine_name():
    """16 is tet-zayin, not yod-vav."""
    assert hebrew.to_hebrew(16) == hebrew.UNITS[9] + hebrew.UNITS[7]
    assert hebrew.from_hebrew(hebrew.to_hebrew(16)) == 16


def test_hebrew_applies_the_rule_inside_larger_numbers():
    assert hebrew.from_hebrew(hebrew.to_hebrew(115)) == 115


def test_hebrew_five_hundred_repeats_tav():
    assert hebrew.to_hebrew(500) == hebrew.HUNDREDS[4] + hebrew.HUNDREDS[1]


def test_hebrew_nine_hundred_repeats_tav_twice():
    assert hebrew.from_hebrew(hebrew.to_hebrew(900)) == 900


@pytest.mark.parametrize("n", list(range(1, 1000, 11)) + [1, 999])
def test_hebrew_round_trips_across_its_range(n):
    assert hebrew.from_hebrew(hebrew.to_hebrew(n)) == n


def test_hebrew_rejects_zero():
    with pytest.raises(ValueError, match="no zero"):
        hebrew.to_hebrew(0)


def test_hebrew_ignores_geresh_marks():
    written = hebrew.to_hebrew(241)
    assert hebrew.from_hebrew(written + hebrew.GERESH) == 241


def test_hebrew_letter_sum_ignores_latin():
    """The unsourced Latin transliteration table was removed."""
    assert hebrew.letter_sum("hello") == 0


# --------------------------------------------------------------- Arabic

def test_arabic_declares_which_order_it_implements():
    assert arabic.ORDER == "eastern"


def test_arabic_matches_hebrew_up_to_four_hundred():
    """The documented relationship, tested as set equality.

    Claim key: abjad-decimal-structure. The two series carry the SAME 22
    values up to 400 -- nine units, nine tens, four hundreds -- so the
    test compares the value sets rather than spot-checking a few.
    """
    hebrew_values = set(hebrew.VALUES.values())
    arabic_values = {v for v in arabic.VALUES.values() if v <= 400}
    assert hebrew_values == arabic_values
    assert len(hebrew_values) == 22


def test_arabic_extends_past_hebrew_to_one_thousand():
    """Where the two series part company: the extra Arabic letters."""
    beyond = sorted(v for v in arabic.VALUES.values() if v > 400)
    assert beyond == [500, 600, 700, 800, 900, 1000]
    assert max(hebrew.VALUES.values()) == 400


def test_arabic_reaches_one_thousand():
    assert max(arabic.VALUES.values()) == 1000


def test_arabic_has_twenty_eight_base_letters():
    assert len(arabic.VALUES) == 28


def test_arabic_variants_resolve_to_their_base_letter():
    for variant, base in arabic.VARIANTS.items():
        assert arabic.value(variant) == arabic.VALUES[base]


@pytest.mark.parametrize("n", [1, 9, 10, 99, 100, 469, 1121, 1443, 1999, 9999])
def test_arabic_round_trips(n):
    assert arabic.from_abjad(arabic.to_abjad(n)) == n


def test_arabic_thousands_repeat_ghayn():
    assert arabic.to_abjad(3000) == arabic.THOUSAND * 3


def test_arabic_rejects_zero():
    with pytest.raises(ValueError, match="no zero"):
        arabic.to_abjad(0)


def test_arabic_names_the_character_it_cannot_read():
    with pytest.raises(ValueError, match="carries no abjad value"):
        arabic.from_abjad("Z")


def test_arabic_letter_sum_is_order_independent():
    word = arabic.to_abjad(1443)
    assert arabic.letter_sum(word) == arabic.letter_sum(word[::-1])


# ---------------------------------------------------------- Sexagesimal

def test_sexagesimal_base_and_sub_base():
    assert sexagesimal.BASE == 60
    assert sexagesimal.SUB_BASE == 10


def test_digit_wedges_exposes_the_sub_base():
    assert sexagesimal.digit_wedges(23) == (2, 3)
    assert sexagesimal.digit_wedges(59) == (5, 9)
    assert sexagesimal.digit_wedges(0) == (0, 0)


def test_digit_wedges_rejects_a_digit_outside_the_base():
    with pytest.raises(ValueError, match="0 through 59"):
        sexagesimal.digit_wedges(60)


def test_every_digit_fits_five_tens_and_nine_units():
    for digit in range(60):
        tens, units = sexagesimal.digit_wedges(digit)
        assert 0 <= tens <= 5
        assert 0 <= units <= 9
        assert tens * 10 + units == digit


def test_wedge_layout_covers_every_place():
    assert sexagesimal.wedge_layout(3725) == [(0, 1), (0, 2), (0, 5)]


def test_time_round_trip():
    triple = sexagesimal.encode_time(3725)
    assert str(triple) == "01:02:05"
    assert sexagesimal.decode_time(triple) == 3725


def test_angle_round_trip():
    triple = sexagesimal.encode_angle(3725)
    assert sexagesimal.decode_angle(triple) == 3725


def test_sexagesimal_string_round_trip():
    assert sexagesimal.from_sexagesimal(sexagesimal.to_sexagesimal(3725)) == 3725


def test_babylonian_fraction_halves_and_thirds():
    assert sexagesimal.babylonian_fraction(1, 2, 1) == [30]
    assert sexagesimal.babylonian_fraction(1, 3, 1) == [20]


def test_terminates_only_for_two_three_and_five():
    for d in (2, 3, 4, 5, 6, 8, 9, 10, 12, 15, 20, 30, 60):
        assert sexagesimal.terminates(d), f"1/{d} should terminate in base 60"
    for d in (7, 11, 13, 14, 49):
        assert not sexagesimal.terminates(d), f"1/{d} should not terminate"


def test_encode_time_rejects_negatives():
    with pytest.raises(ValueError):
        sexagesimal.encode_time(-1)


def test_fingerprint_reports_the_wedge_layout():
    report = sexagesimal.fingerprint(3725)
    assert report["wedge_layout"] == [(0, 1), (0, 2), (0, 5)]
    assert report["sexagesimal"] == "1,02,05"
