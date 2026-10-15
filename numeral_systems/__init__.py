"""
Historical numeral systems -- four attested systems of numerical notation,
implemented as standard-library Python with a citation behind every claim.

THE SYSTEMS (numeral_systems.systems)
  hebrew        additive decimal, alphabetic. 1 to 400.
  greek         additive decimal, alphabetic. 27 values, Milesian.
  arabic        additive decimal, alphabetic. Eastern (mashriqi) abjad.
  sexagesimal   positional, base 60, sub-base 10. No zero sign.

Each gives you value(), an encoder, a decoder and a letter-sum.

AROUND THEM
  chronograms   recording a date inside a word -- verifiable
  interpretive  gematria and isopsephy, documented and dated, NOT
                computed as if they produced facts
  readability   Flesch and Flesch-Kincaid, with the formulas named
  primitives    digital_root, weighted_sum, base-N conversion
  sources       the citation register; the test suite enforces it
  classroom     a lesson per system, each carrying its citations
  codex         the unified high-level API

WHAT THIS LIBRARY DOES NOT DO
It does not compute life path, name, soul, destiny or planetary numbers.
Those belong to early-20th-century numerology, not to ancient notation,
and ``numeral_systems.interpretive`` gives the dating and the sources.
An earlier release (v0.1.0, published as "Ancient Numerics Codex") did
compute them and described them as ancient. That was wrong and it was
corrected rather than quietly dropped: see ``classroom.print_retired()``.

    from numeral_systems import codex
    codex.letter_sums("...")
    codex.readability("A short sentence.")
    print(codex.bibliography())
"""
__version__ = "1.0.0"

from . import codex
from . import classroom
from . import chronograms
from . import interpretive
from . import readability
from . import sources
from .systems import hebrew, greek, arabic, sexagesimal
from .primitives import digital_root, weighted_sum, base_n

__all__ = [
    "codex", "classroom", "chronograms", "interpretive", "readability",
    "sources",
    "hebrew", "greek", "arabic", "sexagesimal",
    "digital_root", "weighted_sum", "base_n",
]
