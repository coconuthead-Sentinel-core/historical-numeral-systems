"""Weighted sum -- positional weighted addition.

A general-purpose primitive, exported for callers building their own
positional schemes. Nothing inside this library consumes it: the four
implemented systems either sum unweighted letter values (the three
alphabetic ones) or use ``base_n`` for place arithmetic (sexagesimal).
Stated plainly so a reader does not go hunting for the call site.
"""
from __future__ import annotations


def weighted_sum(values: list[int], weights: list[int] | None = None) -> int:
    """
    Sum a list of values, optionally with positional weights.
    If weights is None, all weights are 1 (plain sum).

    weighted_sum([1, 2, 3])              -> 6
    weighted_sum([1, 2, 3], [10, 20, 30]) -> 10 + 40 + 90 = 140
    """
    if weights is None:
        return sum(values)
    if len(weights) != len(values):
        raise ValueError(f"weights/values length mismatch: {len(weights)} vs {len(values)}")
    return sum(v * w for v, w in zip(values, weights))
