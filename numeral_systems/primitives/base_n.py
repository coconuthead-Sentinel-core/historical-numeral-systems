"""Alternate-base arithmetic (base-60 sexagesimal especially)."""
from __future__ import annotations


def to_base(n: int, base: int) -> list[int]:
    """
    Convert n to a list of digits in given base, most significant first.
    to_base(3661, 60) -> [1, 1, 1]   (1*3600 + 1*60 + 1 = 3661 sec = 1h 1m 1s)
    to_base(255, 16)  -> [15, 15]
    to_base(0, 10)    -> [0]
    """
    if n < 0:
        raise ValueError(f"to_base requires n >= 0; got {n}")
    if base < 2:
        raise ValueError(f"base must be >= 2; got {base}")
    if n == 0:
        return [0]
    digits: list[int] = []
    while n > 0:
        digits.append(n % base)
        n //= base
    return list(reversed(digits))


def from_base(digits: list[int], base: int) -> int:
    """
    Inverse of to_base.
    from_base([1, 1, 1], 60) -> 3661
    from_base([15, 15], 16)  -> 255
    """
    if base < 2:
        raise ValueError(f"base must be >= 2; got {base}")
    n = 0
    for d in digits:
        if d < 0 or d >= base:
            raise ValueError(f"digit {d} out of range for base {base}")
        n = n * base + d
    return n


def sexagesimal_string(n: int) -> str:
    """
    Format an integer in Mesopotamian sexagesimal notation: "1,30,5"
    means 1*3600 + 30*60 + 5.
    Useful for time, angles, and historical calendar work.

    sexagesimal_string(3725) -> '1,02,05'   (1h 2m 5s)
    sexagesimal_string(0)    -> '0'
    """
    digits = to_base(n, 60)
    return ",".join(f"{d:02d}" if i > 0 else str(d) for i, d in enumerate(digits))
