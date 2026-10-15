# Method

How this library's claims are controlled, and what that control does and
does not achieve.

## The problem this addresses

Software about historical subjects makes two kinds of assertion, and they
fail in different ways.

A **computational** assertion — that this table round-trips, that this digit
decomposes — is checkable by running the code. A test either passes or it
does not.

A **historical** assertion — that these letters were used as numerals, that
this practice dates from the 14th century — is not checkable by running
anything. Code can be internally perfect and historically false. The first
release of this library was exactly that: the tests passed, and the README
described modern numerology as a primordial mathematical tradition.

Ordinary software practice has no mechanism for the second kind. This
library adds one.

## The mechanism

**1. Claims are enumerated, not scattered.** Every historical assertion the
library makes is declared once, as a key in `CLAIMS` in
`numeral_systems/sources.py`, with its wording. Modules and lessons refer to
claims by key.

**2. Citations are structured.** Each entry in `CITATIONS` names the source
and lists the claim keys it supports.

**3. A test enforces the join.** `tests/test_sources.py` fails the build if:

- a declared claim has no supporting citation (`uncited_claims`)
- a citation names a claim nobody declares (`orphan_supports`)
- a lesson references a claim key that does not exist
- a claim rests on a popular-tier source alone
- one of the three most contestable claims lacks a scholarly source

This is the point of the design. The rule is not a promise in a contributing
guide that a reviewer has to remember to apply; it is a failing test.

**4. Verification depth is declared separately from source quality.** Two
fields, deliberately not collapsed into one:

- `tier` — what kind of source it is: `scholarly`, `reference`,
  `collection`, `popular`.
- `verification` — how far *this release* actually checked it: `consulted`
  (read directly), `bibliographic` (details confirmed, source is the
  recognised authority, pages not read), `reported` (known through
  secondary summaries only).

A correct citation to the right book is still, implicitly, a claim about
one's own diligence. Separating the axes stops that claim from being made by
accident. Most entries here are `bibliographic`, and a test requires each
one to say so in its own prose as well as in its field, so a reader skimming
the bibliography cannot miss it.

**5. The gap is published.** `unverified_claims()` lists every claim that no
directly-read source supports; `reading_list()` prints the books that would
close it. This appears in `docs/SOURCES.md` under *Open reading list*. The
limitation is a section of the documentation rather than something a reader
has to infer.

**6. Execution-checked claims are marked as such.** `EXECUTION_CHECKED`
records which claims the tests additionally prove by running code — that the
Greek code points round-trip, that every sexagesimal digit decomposes and
recomposes. This is kept separate from citation on purpose: a table being
internally consistent is not evidence that it matches the historical record.

**7. Derived documents are generated.** `docs/SOURCES.md` is produced by
`tools/generate_sources_doc.py` from the register, and CI diffs the
committed file against a fresh generation. The document cannot drift from
the code.

## What this achieves

- No historical claim ships uncited.
- The strength of the evidence behind each claim is legible without reading
  the source code.
- The library's own unverified residue is a published artefact.
- A reviewer can audit the evidence base by reading one file.

## What this does not achieve

It is worth being plain about the limits, because the mechanism could
otherwise be mistaken for more than it is.

- **It does not verify that a cited source says what it is cited for.** A
  `bibliographic` entry asserts that the source is the recognised authority,
  not that its pages were checked. Closing that gap requires a library and a
  reader, and the register names which books.
- **It does not police prose.** The gate covers the claim register and the
  classroom lesson data. Explanatory text in docstrings is reviewed by a
  human, not by a test. A false sentence in a docstring would pass.
- **It cannot adjudicate scholarly disagreement.** Where sources conflict —
  the origin of base 60, the dating of the Hebrew adoption — the library
  states that they conflict and declines to pick. That is a policy, not a
  resolution.
- **Tier is assigned by judgement.** Nothing verifies that a source labelled
  `scholarly` deserves the label.

## Extending it

Adding a historical claim means four things, in this order:

1. Declare the claim in `CLAIMS` with its wording.
2. Add or extend a `CITATIONS` entry listing the claim in `supports`, with
   an honest `verification` level — and if it is `bibliographic`, include
   the required disclosure sentence in the note.
3. Reference the claim key from the module or lesson that asserts it.
4. Regenerate `docs/SOURCES.md`.

Run `pytest -q`. If the claim is unsupported, the build will say so before
anyone else does.

## Standards frame

The discipline here is ordinary engineering practice applied to evidence:
a declared requirement, a mechanism that enforces it, and an honest record
of what the mechanism does not cover. The citation style throughout is
Chicago notes-bibliography, author-first.
