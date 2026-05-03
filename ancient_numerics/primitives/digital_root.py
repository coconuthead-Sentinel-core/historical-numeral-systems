"""Digital root — iterative sum-of-digits collapse."""
from __future__ import annotations


def digital_root(n: int) -> int:
    """
    Reduce n to a single digit by summing digits iteratively.
    digital_root(1234) -> 1+2+3+4=10 -> 1+0=1
    digital_root(0)    -> 0
    digital_root(9)    -> 9
    digital_root(99)   -> 9
    """
    if n < 0:
        raise ValueError(f"digital_root requires n >= 0; got {n}")
    if n == 0:
        return 0
    # The "casting out nines" identity: digital_root(n) = 1 + (n-1) mod 9
    return 1 + (n - 1) % 9


def digital_root_steps(n: int) -> list[int]:
    """Return every intermediate sum on the way to the root."""
    if n < 0:
        raise ValueError(f"digital_root_steps requires n >= 0; got {n}")
    steps = [n]
    while steps[-1] >= 10:
        steps.append(sum(int(d) for d in str(steps[-1])))
    return steps
