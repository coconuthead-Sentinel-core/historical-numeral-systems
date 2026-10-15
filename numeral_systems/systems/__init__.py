"""
The numeral systems themselves -- notation for representing quantity.

Three are additive and alphabetic: ``hebrew``, ``greek``, ``arabic``. One
is positional: ``sexagesimal``.

Interpretive practices that use the same letter values to read meaning out
of words live in ``numeral_systems.interpretive``, deliberately outside
this package. Claim key: ``notation-is-not-interpretation``.
"""
from . import hebrew, greek, arabic, sexagesimal

__all__ = ["hebrew", "greek", "arabic", "sexagesimal"]
