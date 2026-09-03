# Ancient Numerics Codex

> Five primordial mathematical traditions — **Hebrew Gematria**, **Greek Isopsephy / Pythagorean numerology**, **Arabic Abjad**, **Indian/Vedic numerology**, and **Mesopotamian sexagesimal metrology** — brought to 2026 AI-tooling standards as composable Python primitives.

![Status](https://img.shields.io/badge/status-public-success)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)

---

## Why this exists

These five traditions are humanity's oldest functional number-systems. Each
one solved a real problem (text fingerprinting, complexity scoring, date
encoding, fractional arithmetic) using primitives that map cleanly onto
modern computer-science concepts.

| Tradition | Modern CS analog |
|---|---|
| **Hebrew Gematria** | Character→integer hash + sum (deterministic content fingerprinting) |
| **Greek Isopsephy / Pythagorean** | Weighted positional hashing (polynomial rolling hash) |
| **Arabic Abjad** | Date encoding via word selection (mnemonic hex / vanity strings) |
| **Indian / Vedic numerology** | Tokenization + complexity scoring (NLP readability metrics) |
| **Mesopotamian sexagesimal** | Alternate-base arithmetic (base-60 still used for time + angles) |

This library packages all five as a **tooling library for AI-assisted code
generation**. Use `glyph_id()` to derive content-meaningful document IDs.
Use `complexity_score()` to auto-classify cognitive load. Use `to_sexagesimal()`
to render time/angle values in Babylonian notation.

## Install

```bash
pip install -e .
# or
pip install -e ".[dev]"   # includes pytest
```

## Quick start

```python
from ancient_numerics import codex

# Generate a content-meaningful document ID (NLCA-compatible regex)
print(codex.glyph_id("CSTM", "EVENT", "lattice intake"))
# -> e.g. 'CSTM-EVENT-413'

# Score cognitive complexity (1-10) with NLCA zone
print(codex.complexity_score("a sentence with several syllables"))
# -> {'score_1_10': 4, 'syllable_count': 12, 'nlca_zone': 'YELLOW', ...}

# Run text through all 5 traditions at once
print(codex.fingerprint("hello world"))

# Render the current time as Babylonian sexagesimal
print(codex.encode_now_sexagesimal())
```

## API surface

### `ancient_numerics.codex` — unified high-level API

| Function | Returns |
|---|---|
| `fingerprint(text)` | dict with all 5 tradition readings |
| `glyph_id(prefix, subtype, content)` | NLCA-compatible doc_id like `'CSTM-EVENT-413'` |
| `complexity_score(text)` | dict with 1-10 score + NLCA zone |
| `encode_now_sexagesimal()` | current UTC time in Babylonian form |
| `primer()` | quick-reference card (string) |

### Per-tradition modules — `ancient_numerics.traditions.*`

```python
from ancient_numerics.traditions import gematria, isopsephy, abjad, vedic, metrology

gematria.sum_word("אדם")              # 45
isopsephy.psephos("λογος")             # 373
abjad.chronogram("ا", 1)               # {'matches': True, ...}
vedic.syllable_count("beautiful")      # 3
metrology.to_sexagesimal(3725)         # '1,02,05'  (1h 2m 5s)
```

### Reusable primitives — `ancient_numerics.primitives.*`

```python
from ancient_numerics.primitives import digital_root, weighted_sum, to_base, from_base

digital_root(1234)                    # 1
weighted_sum([1, 2, 3], [10, 20, 30]) # 140
to_base(3661, 60)                     # [1, 1, 1]
```

## Classroom mode

Each tradition has historical context + modern analog + code example + exercise:

```python
from ancient_numerics import classroom
print(classroom.print_lesson("gematria"))
# === Hebrew Gematria ===
# Origin:        Late antiquity; codified in Kabbalah
# Core method:   Each Hebrew letter has a numeric value...
# Modern analog: Character->integer hash + sum...
# Code example:  from ancient_numerics.traditions import gematria; ...
# Exercise:      Verify: word A and its anagram have the same gematria sum.

print(classroom.print_all())  # all 5 lessons
```

## Tests

```bash
pytest -v
```

Currently: **52 tests across 3 test files**, covering primitives, traditions, and the unified codex API.

## Project structure

```
Ancient Numerics Codex/
├── README.md
├── LICENSE
├── pyproject.toml
├── .gitignore
├── ancient_numerics/
│   ├── __init__.py
│   ├── codex.py              ← unified high-level API
│   ├── classroom.py          ← teaching helpers
│   ├── primitives/
│   │   ├── digital_root.py   ← iterative digit-sum collapse
│   │   ├── weighted_sum.py   ← positional weighted addition
│   │   └── base_n.py         ← alternate-base arithmetic + sexagesimal
│   └── traditions/
│       ├── gematria.py       ← Hebrew letter→int + reduction
│       ├── isopsephy.py      ← Greek/Pythagorean values + life path
│       ├── abjad.py          ← Arabic letter values + chronograms
│       ├── vedic.py          ← syllable counter + planetary numerology
│       └── metrology.py      ← Mesopotamian base-60 (time/angles)
└── tests/
    ├── test_primitives.py
    ├── test_traditions.py
    └── test_codex.py
```

## Integration with the broader portfolio

This library is designed to be used as **a tool the AI assistant calls during
code generation** — not as a runtime service. Specifically:

- `codex.glyph_id()` produces NLCA-schema-compatible `doc_id` values that match the regex `^[A-Z]{3,4}-[A-Z]{3,6}-[0-9]{3}$`
- `codex.complexity_score()` produces NLCA-zone classifications (`GREEN`/`YELLOW`/`RED`) usable directly by the CSTM_Lattice 8-node pipeline
- `metrology.to_sexagesimal()` provides timestamp formatting that survives timezone confusion (a known issue in distributed systems)
- The classroom module makes this library educational artifact in addition to a working tool — useful for the proprietor's xAI AI Tutor work

## License

MIT — see [`LICENSE`](LICENSE).

## Author

**Shannon Brian Kelley** — AI Orchestrator Architect.
Built in collaboration with Claude AI (Anthropic) under file-system-bound persona protocol; co-creator role attributed as "Archivist of Wisdom."

Canon entry **#19** in the architect's portfolio.
