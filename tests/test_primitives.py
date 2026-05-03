"""Tests for the three reusable primitives."""
import pytest
from ancient_numerics.primitives import (
    digital_root, digital_root_steps, weighted_sum,
    to_base, from_base, sexagesimal_string,
)


class TestDigitalRoot:
    def test_zero(self):
        assert digital_root(0) == 0

    def test_single_digit_unchanged(self):
        for n in range(10):
            assert digital_root(n) == n

    def test_known_examples(self):
        assert digital_root(1234) == 1   # 1+2+3+4=10 -> 1+0=1
        assert digital_root(99) == 9     # 9+9=18 -> 1+8=9
        assert digital_root(38) == 2     # 3+8=11 -> 1+1=2

    def test_multiples_of_9_reduce_to_9(self):
        for k in range(1, 20):
            assert digital_root(9 * k) == 9

    def test_negative_raises(self):
        with pytest.raises(ValueError):
            digital_root(-1)

    def test_steps_progression(self):
        steps = digital_root_steps(9999)
        assert steps[0] == 9999
        assert steps[-1] < 10
        # Each step should be smaller than the previous
        for i in range(1, len(steps)):
            assert steps[i] < steps[i-1]


class TestWeightedSum:
    def test_no_weights_is_plain_sum(self):
        assert weighted_sum([1, 2, 3]) == 6

    def test_with_weights(self):
        assert weighted_sum([1, 2, 3], [10, 20, 30]) == 140

    def test_empty(self):
        assert weighted_sum([]) == 0

    def test_mismatched_lengths(self):
        with pytest.raises(ValueError):
            weighted_sum([1, 2], [10, 20, 30])


class TestBaseN:
    def test_to_base_10(self):
        assert to_base(123, 10) == [1, 2, 3]

    def test_to_base_60(self):
        assert to_base(3661, 60) == [1, 1, 1]   # 1*3600 + 1*60 + 1
        assert to_base(3725, 60) == [1, 2, 5]   # 1h 2m 5s
        assert to_base(60, 60) == [1, 0]

    def test_to_base_zero(self):
        assert to_base(0, 10) == [0]

    def test_to_base_16(self):
        assert to_base(255, 16) == [15, 15]

    def test_round_trip(self):
        for n in [0, 1, 7, 60, 100, 3661, 99999]:
            for base in [2, 8, 10, 16, 60]:
                assert from_base(to_base(n, base), base) == n

    def test_negative_raises(self):
        with pytest.raises(ValueError):
            to_base(-1, 10)
        with pytest.raises(ValueError):
            from_base([1, 2], 1)

    def test_invalid_digit_in_from_base(self):
        with pytest.raises(ValueError):
            from_base([60], 60)  # 60 is out of range for base 60

    def test_sexagesimal_string(self):
        assert sexagesimal_string(0) == "0"
        assert sexagesimal_string(60) == "1,00"
        assert sexagesimal_string(3725) == "1,02,05"
