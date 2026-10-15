# Historical Numeral Systems

> Four attested systems of **numerical notation** — Hebrew, Greek Milesian and
> Arabic abjad alphabetic numerals, plus Mesopotamian sexagesimal — implemented
> as standard-library Python, with a citation register that the test suite
> enforces.

[![CI](https://github.com/coconuthead-Sentinel-core/historical-numeral-systems/actions/workflows/ci.yml/badge.svg)](https://github.com/coconuthead-Sentinel-core/historical-numeral-systems/actions/workflows/ci.yml)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.10%20–%203.13-blue)
![Dependencies](https://img.shields.io/badge/runtime%20dependencies-none-brightgreen)

---

## What this is

Three of these systems are **additive and alphabetic**: the letters of the
script double as its numerals. One, the Mesopotamian, is **positional** — the
earliest positional notation known. All four were used for ordinary counting
and dating, and each is implemented here with an encoder, a decoder, a
character-value lookup, and tests that round-trip across its range.

The library is standard-library only. There are no runtime dependencies.

## What this is not

It does **not** compute life path numbers, name numbers, soul or destiny
numbers, or planetary correspondences for the digits 1 to 9. Those belong to
**numerology**, which is a different subject from numerical notation, and
`numeral_systems/interpretive.py` gives the dating and the sources rather than
leaving the omission unexplained.

Gematria and isopsephy are documented in that same module as **interpretive
practices** — techniques for reading meaning out of a text — and kept out of
the `systems` package, which is about representing quantity.

## Correction notice — v0.1.0 to v1.0.0

The first release of this library was published as *"Ancient Numerics Codex —
five primordial mathematical traditions."* That framing was wrong, and the
errors under it were not only editorial. They are listed here rather than
quietly removed, because a library that corrects itself in the open is worth
more than one that appears never to have been wrong.

**Factual:**

- **"Five primordial mathematical traditions"** — only one of the five was a
  mathematical notation. Gematria and isopsephy are interpretive practices;
  the other two entries were modern numerology.
- **"Pythagorean numerology," dated to the 6th century BCE** — the
  name-and-birth-date method is early-20th-century and American, originating
  with L. Dow Balliett. The Pythagorean label is borrowed.
- **"Indian / Vedic numerology," described as ancient** — unsupported in the
  scholarly record. No Vedic text sets out these correspondences. The modern
  practice is best described as a synthesis of jyotish vocabulary, the Chinese
  Lo Shu grid, and Western name-number methods. This is a gap in the evidence
  rather than a demonstrated forgery, and the library now says so in those
  terms.
- **Syllable counting presented as Sanskrit prosody** — the counter is an
  English vowel-cluster heuristic. It is now in `readability.py` under the
  published formulas it actually serves.

**Functional:**

- **The Greek table was missing three letters.** The Milesian system needs 27
  values and the Greek alphabet supplies 24, so **stigma (6), koppa (90) and
  sampi (900)** carry the remainder. All three were absent, which made 6, 90,
  900 and every number containing them unrepresentable. `tests/test_systems.py`
  now guards each one.
- **`complexity_score` inverted its own bands** — it returned its most
  permissive label, `GREEN`, for its most complex input.
- **`complexity_score` was contaminated by noise** — it added the gematria sum
  modulo 7 to the score, an arbitrary swing of 0 to 6 on a 1-to-10 scale.
- **`glyph_id` was described as a content fingerprint.** It derived three
  digital roots from letter-sums, which are order-independent, so anagrams
  collided by construction. It now uses BLAKE2b and publishes its own
  collision bound.
- **`chronogram_year()` did nothing.** It returned the current calendar year
  and never touched an abjad value.
- **The Latin transliteration tables were invented.** Real romanization
  standards exist — ISO 259 for Hebrew, ISO 233 and DIN 31635 for Arabic — and
  the tables matched none of them. They were removed; the letter-sum of a
  Latin string is now correctly zero.

`numeral_systems.classroom.print_retired()` prints this record from code, and
[`CHANGELOG.md`](CHANGELOG.md) itemises every removal and rename.

The mechanism added so this cannot recur quietly is described in
[`docs/METHOD.md`](docs/METHOD.md): claims are enumerated, citations are
structured, and a test enforces the join.

## Install

```bash
pip install -e .
pip install -e ".[dev]"   # adds pytest
```

## Quick start

```python
from numeral_systems.systems import greek, hebrew, arabic, sexagesimal

greek.to_greek(241)              # sigma-mu-alpha  (200 + 40 + 1)
greek.to_greek(900)              # sampi — absent from v0.1.0
greek.from_greek(greek.to_greek(96)) == 96

hebrew.to_hebrew(15)             # tet-vav, not yod-he: avoids a divine name
arabic.to_abjad(1443)            # eastern (mashriqi) order
sexagesimal.digit_wedges(23)     # (2, 3) — the sub-base of 10, made explicit
```

```python
from numeral_systems import codex

codex.readability("A short sentence.")      # Flesch, Flesch-Kincaid, band
codex.glyph_id("CSTM", "EVENT", "intake")   # hashed id, order-sensitive
codex.collision_probability(38)             # ~0.5 — know this before using it
print(codex.bibliography())                 # every source, by tier
```

## The four systems

Each lives in `numeral_systems/systems/` and exposes `value()`, an encoder, a
decoder and a letter-sum.

**`hebrew`** — additive, decimal, non-positional. Nine units, nine tens, four
hundreds, ending at 400 because the alphabet has 22 letters. Adapted from the
Greek system; the earliest archaeological evidence is late second century BCE.
Values above 400 repeat tav. Final (sofit) forms carry their ordinary values.
15 and 16 are written tet-vav and tet-zayin rather than yod-he and yod-vav,
because those spellings would form divine names — the encoder honours that
rule, including inside larger numbers.

**`greek`** — additive, decimal, non-positional. Twenty-seven values in three
ranks of nine, attested from roughly the 6th century BCE. Three letters
outside the classical alphabet carry 6, 90 and 900. Thousands reuse the unit
letters behind the lower numeral sign.

**`arabic`** — additive, decimal, non-positional. The 28 letters in old
alphabetic (abjad) order. Values match the Hebrew series to 400, then run 500
to 1000. This module implements the **eastern (mashriqi)** order and says so in
`arabic.ORDER`, because the Maghrebi order assigns several later letters
different values and mixing the two silently would corrupt a date reading.

**`sexagesimal`** — **positional**, base 60, with a sub-base of 10 inside each
digit: two wedge signs, one counting tens and one counting units, compose all
59 non-zero digits. There was no true zero sign, so magnitude had to come from
context. `terminates()` reports which unit fractions terminate in base 60 — a
property, stated as a property rather than as the Mesopotamians' motive, since
the historical origin of the base is disputed.

## Around them

| Module | What it does |
|---|---|
| `chronograms` | Recording a date inside a word. Verifiable: the sum either equals the year or it does not. |
| `interpretive` | Gematria and isopsephy, documented and dated. Includes a collision demonstration showing why a letter-sum cannot identify a word. |
| `readability` | Flesch Reading Ease and Flesch-Kincaid Grade Level, with both formulas cited. |
| `primitives` | `digital_root`, `weighted_sum`, base-N conversion. Pure number theory, no claims attached. |
| `sources` | The citation register. Every claim keys into it. |
| `classroom` | One lesson per system, each carrying its own citations and an explicit "is NOT" line. |
| `codex` | The unified high-level API. |

## Chronograms

A chronogram encodes a year in the abjad values of a phrase. The practice is
well attested in Persian and Urdu literature, where it is called *madda
tarikh*. Early poets wrote years out in words; later they used letter values,
and from around the turn of the 14th century organised those values into
meaningful phrases, a technique called *hisab al-jummal*. It was used for
births, deaths, appointments, marriages, buildings, war and peace.

```python
from numeral_systems import chronograms

chronograms.compose_hint(469)        # the letter skeleton for 469 AH
chronograms.verify(phrase, 469)      # matches, and the signed delta if not
chronograms.approximate_ce(469)      # orientation only — see the docstring
```

Years in this tradition are Hijri. Converting AH to CE exactly needs a
calendar implementation this library does not carry, since the Hijri year is
lunar; `approximate_ce` is named for what it is.

## Classroom mode

```python
from numeral_systems import classroom

print(classroom.print_lesson("greek"))   # type, period, method, is-NOT, sources
print(classroom.print_all())
print(classroom.print_retired())         # what was removed on verification
```

Every lesson names its claim keys, and the suite fails the build if a key has
no entry in the register. A lesson cannot assert something unsourced.

## Sources, and how far they were checked

`numeral_systems.sources` holds the register. Every historical claim the
library makes is declared there once and referenced by key, and
[`tests/test_sources.py`](tests/test_sources.py) fails the build if a claim
has no citation, if a citation names a claim nobody makes, or if a claim
rests on a popular-tier source alone. The full design, and its limits, are in
[`docs/METHOD.md`](docs/METHOD.md).

Each citation carries **two** labels, deliberately not collapsed into one:

- **tier** — what kind of source it is: `scholarly`, `reference`,
  `collection`, `popular`.
- **verification** — how far *this release* actually checked it:
  `consulted` (read directly), `bibliographic` (details confirmed and the
  source is the recognised authority, but its pages were **not** read for
  this release), or `reported` (known only through secondary summaries).

**Most entries here are `bibliographic`, and the library says so rather than
implying otherwise.** A correct citation to the right book is still,
implicitly, a claim about one's own diligence, and separating the two axes
stops that claim from being made by accident. `sources.unverified_claims()`
lists every claim that no directly-read source supports, and
`sources.reading_list()` prints the books that would close the gap. Both
appear in [`docs/SOURCES.md`](docs/SOURCES.md) under *Open reading list*.

The one exception is the Unicode Standard, marked `consulted`: every code
point this library hard-codes also round-trips in the test suite, so the
Greek assignments are checked by execution as well as by citation.

The spine of the library is:

- Chrisomalis, Stephen. *Numerical Notation: A Comparative History.*
  Cambridge University Press, 2010. Surveys more than 100 attested systems
  across roughly 5,500 years.
- Chrisomalis, Stephen. *Reckonings: Numerals, Cognition, and History.*
  MIT Press, 2021.
- Dudley, Underwood. *Numerology: Or, What Pythagoras Wrought.* Mathematical
  Association of America, 1997.
- Plofker, Kim. *Mathematics in India.* Princeton University Press, 2009.
- *Encyclopaedia Iranica*, "Chronograms."
- The Unicode Standard, for the code points of stigma, koppa and sampi.

The primary cuneiform material is held chiefly by the **British Museum**, the
**Louvre**, and the **Vorderasiatisches Museum** in Berlin.

Run `print(codex.bibliography())` for the full register with notes.

## Tests

```bash
pytest -q
```

**383 test cases pass** across four files, on Python 3.10 through 3.13 in CI.
The count is inflated by parametrization — `test_systems.py` round-trips each
system across sampled ranges — so treat it as coverage breadth rather than as
383 distinct assertions. `tests/test_sources.py` is the static gate on
citations, and several tests in `test_systems.py` and `test_codex.py` are
labelled in their docstrings as regression guards against the v0.1.0 defects
listed above.

CI additionally runs the citation gate as its own step, in case the suite is
ever skipped or renamed, and diffs `docs/SOURCES.md` against a fresh
generation so the document cannot drift from the register.

## Project structure

```
historical-numeral-systems/
├── README.md
├── CHANGELOG.md
├── LICENSE
├── pyproject.toml
├── .github/workflows/ci.yml
├── docs/
│   ├── METHOD.md             ← how claims are controlled, and the limits
│   ├── MIRRORS.md            ← the three copies and how to check them
│   ├── SOURCES.md            ← generated from the register
│   └── mirror-manifest.json
├── tools/
│   ├── generate_sources_doc.py
│   └── verify_mirrors.py
├── numeral_systems/
│   ├── __init__.py
│   ├── codex.py              ← unified API
│   ├── sources.py            ← citation register
│   ├── classroom.py          ← lessons + the retired record
│   ├── chronograms.py        ← date encoding (verifiable)
│   ├── interpretive.py       ← gematria / isopsephy, documented
│   ├── readability.py        ← Flesch + Flesch-Kincaid
│   ├── primitives/
│   │   ├── digital_root.py
│   │   ├── weighted_sum.py
│   │   └── base_n.py
│   └── systems/
│       ├── hebrew.py
│       ├── greek.py
│       ├── arabic.py
│       └── sexagesimal.py
└── tests/
    ├── test_primitives.py
    ├── test_systems.py
    ├── test_codex.py
    └── test_sources.py
```

## Mirrors

This repository is kept in three places: **GitHub** (the source of truth), a
**laptop working clone**, and an **off-machine `git bundle` in Google Drive**.
`python tools/verify_mirrors.py` checks that they agree and distinguishes an
archive that is merely *behind* from one that has genuinely *diverged*.

[`docs/MIRRORS.md`](docs/MIRRORS.md) has the protocol, the recovery order for
when GitHub goes sideways, and the known limits — including the important one:
the laptop clone lives inside the OneDrive sync root, so the laptop and cloud
copies are **one point wearing two hats**, not two.

## License

MIT — see [`LICENSE`](LICENSE).

## Author

**Shannon Brian Kelley.** Written with AI assistance (Claude, Anthropic);
the historical claims were verified against the sources listed above before
this release, and the v0.1.0 claims that failed that check are documented in
the correction notice rather than removed silently.
