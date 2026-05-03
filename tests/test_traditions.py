"""Tests for the five traditions."""
import pytest
from ancient_numerics.traditions import gematria, isopsephy, abjad, vedic, metrology


class TestGematria:
    def test_hebrew_letter_values(self):
        assert gematria.value("א") == 1
        assert gematria.value("י") == 10
        assert gematria.value("ק") == 100
        assert gematria.value("ת") == 400

    def test_hebrew_word_sum(self):
        # אדם (Adam) = 1 + 4 + 40 = 45
        assert gematria.sum_word("אדם") == 45

    def test_unknown_char_returns_zero(self):
        assert gematria.value("@") == 0
        assert gematria.value(" ") == 0

    def test_latin_transliteration(self):
        assert gematria.value("a") == 1   # a -> aleph
        assert gematria.value("y") == 10  # y -> yod

    def test_reduce_returns_single_digit(self):
        for word in ["abc", "hello", "אדם", "test"]:
            r = gematria.reduce(word)
            assert 0 <= r <= 9

    def test_fingerprint_shape(self):
        fp = gematria.fingerprint("hello")
        assert "sum" in fp
        assert "digital_root" in fp
        assert "char_count" in fp


class TestIsopsephy:
    def test_pythagorean_a_to_z(self):
        # a=1, b=2, ..., i=9, j=1, k=2, ..., z=8
        assert isopsephy.pythagorean_value("a") == 1
        assert isopsephy.pythagorean_value("i") == 9
        assert isopsephy.pythagorean_value("j") == 1
        assert isopsephy.pythagorean_value("z") == 8

    def test_greek_milesian(self):
        assert isopsephy.greek_value("α") == 1
        assert isopsephy.greek_value("β") == 2
        assert isopsephy.greek_value("ω") == 800

    def test_psephos_logos(self):
        # λ + ο + γ + ο + σ = 30 + 70 + 3 + 70 + 200 = 373
        assert isopsephy.psephos("λογος") == 373

    def test_value_falls_back_to_pythagorean_for_latin(self):
        assert isopsephy.value("a") == 1
        assert isopsephy.value("α") == 1

    def test_life_path_returns_1_to_9(self):
        for name in ["alice", "bob", "charlie", "shannon"]:
            r = isopsephy.life_path_number(name)
            assert 1 <= r <= 9

    def test_fingerprint_shape(self):
        fp = isopsephy.fingerprint("logos")
        assert "greek_psephos" in fp
        assert "pythagorean_sum" in fp
        assert "life_path" in fp
        assert "digital_root" in fp


class TestAbjad:
    def test_arabic_letter_values(self):
        assert abjad.value("ا") == 1
        assert abjad.value("ك") == 20
        assert abjad.value("غ") == 1000

    def test_latin_transliteration(self):
        assert abjad.value("a") == 1
        assert abjad.value("k") == 20

    def test_chronogram_match(self):
        result = abjad.chronogram("ا", 1)
        assert result["matches"] is True
        assert result["delta"] == 0

    def test_chronogram_mismatch(self):
        result = abjad.chronogram("ا", 1442)
        assert result["matches"] is False
        assert result["delta"] == 1 - 1442

    def test_fingerprint_shape(self):
        fp = abjad.fingerprint("ابجد")
        assert "abjad_sum" in fp
        assert "digital_root" in fp


class TestVedic:
    def test_syllable_count_simple(self):
        assert vedic.syllable_count("a") == 1
        assert vedic.syllable_count("hello") == 2  # he-llo
        assert vedic.syllable_count("beautiful") >= 3

    def test_syllable_count_multiple_words(self):
        assert vedic.syllable_count("hello world") == 3  # he-llo + world

    def test_life_number_in_range(self):
        for name in ["alice", "bob", "shannon"]:
            r = vedic.life_number(name)
            assert 1 <= r <= 9

    def test_destiny_number_in_range(self):
        r = vedic.destiny_number("hello world")
        assert 1 <= r <= 9

    def test_soul_number_in_range(self):
        r = vedic.soul_number("alice")
        assert 1 <= r <= 9

    def test_number_meaning_has_planet(self):
        for n in range(1, 10):
            m = vedic.number_meaning(n)
            assert "planet" in m
            assert "quality" in m

    def test_fingerprint_shape(self):
        fp = vedic.fingerprint("shannon")
        assert "syllable_count" in fp
        assert "life_number" in fp
        assert "destiny_number" in fp
        assert "soul_number" in fp


class TestMetrology:
    def test_encode_time(self):
        t = metrology.encode_time(3725)  # 1h 2m 5s
        assert t.hours == 1
        assert t.minutes == 2
        assert t.seconds == 5

    def test_time_str_format(self):
        t = metrology.encode_time(3725)
        assert str(t) == "01:02:05"

    def test_encode_decode_round_trip(self):
        for n in [0, 1, 60, 3600, 3725, 86399]:
            t = metrology.encode_time(n)
            assert metrology.decode_time(t) == n

    def test_encode_angle(self):
        a = metrology.encode_angle(3725)
        assert a.degrees == 1
        assert a.arcmin == 2
        assert a.arcsec == 5

    def test_to_sexagesimal(self):
        assert metrology.to_sexagesimal(0) == "0"
        assert metrology.to_sexagesimal(3725) == "1,02,05"

    def test_from_sexagesimal_round_trip(self):
        for n in [0, 60, 3725, 86399, 99999]:
            s = metrology.to_sexagesimal(n)
            assert metrology.from_sexagesimal(s) == n

    def test_babylonian_fraction_half(self):
        result = metrology.babylonian_fraction(1, 2, 1)
        assert result == [30]   # 1/2 = 30/60

    def test_babylonian_fraction_third(self):
        result = metrology.babylonian_fraction(1, 3, 2)
        assert result == [20, 0]   # 1/3 = 20/60

    def test_negative_raises(self):
        with pytest.raises(ValueError):
            metrology.encode_time(-1)
        with pytest.raises(ValueError):
            metrology.encode_angle(-1)
        with pytest.raises(ValueError):
            metrology.babylonian_fraction(1, 0)

    def test_fingerprint_shape(self):
        fp = metrology.fingerprint(3725)
        assert "sexagesimal" in fp
        assert "time_form" in fp
        assert "angle_form" in fp
