# Sources

> Generated from `numeral_systems/sources.py`. Do not edit by hand --
> edit the register and regenerate, so this document cannot drift from
> the code the test suite checks.

Every historical claim this library makes is listed below with the
citations supporting it. `tests/test_sources.py` fails the build if a
claim has no citation, if a citation names a claim nobody makes, or if
a claim rests on a popular-tier source alone.

## Claims

### `abjad-decimal-structure`

The Arabic abjad numerals match the Hebrew values up to 400; the additional Arabic letters carry 500 through 1000.

- **[chrisomalis2010]** (scholarly) Chrisomalis, Stephen. Numerical Notation: A Comparative History. Cambridge: Cambridge University Press, 2010. ISBN 978-0-521-87818-0.

### `alphabetic-numerals-are-numeral-systems`

Hebrew, Greek and Arabic letters were used as numerals for ordinary counting and dating. These are numeral systems.

- **[chrisomalis2010]** (scholarly) Chrisomalis, Stephen. Numerical Notation: A Comparative History. Cambridge: Cambridge University Press, 2010. ISBN 978-0-521-87818-0.

### `chronogram-phrase-era`

Organising abjad values into meaningful phrases dates from around the turn of the 14th century.

- **[iranica-chronograms]** (reference) 'Chronograms' (madda tarikh). Encyclopaedia Iranica. https://www.iranicaonline.org/

### `chronograms-attested`

Encoding a date in the abjad values of a word or phrase is an attested historical practice in Persian and Urdu literature.

- **[iranica-chronograms]** (reference) 'Chronograms' (madda tarikh). Encyclopaedia Iranica. https://www.iranicaonline.org/

### `greek-milesian-structure`

The Greek Milesian system is additive and decimal: nine units, nine tens, nine hundreds, for 27 values in all.

- **[chrisomalis2010]** (scholarly) Chrisomalis, Stephen. Numerical Notation: A Comparative History. Cambridge: Cambridge University Press, 2010. ISBN 978-0-521-87818-0.
- **[unicode]** (reference) The Unicode Standard. Unicode Consortium. https://www.unicode.org/versions/latest/

### `greek-obsolete-letters`

Because the Greek alphabet has 24 letters and the system needs 27 values, three letters outside the classical alphabet carry 6, 90 and 900: stigma, koppa and sampi.

- **[unicode]** (reference) The Unicode Standard. Unicode Consortium. https://www.unicode.org/versions/latest/

### `hebrew-from-greek`

The Hebrew alphabetic numerals were adapted from the Greek system; with 22 letters the series stops at 400.

- **[chrisomalis2010]** (scholarly) Chrisomalis, Stephen. Numerical Notation: A Comparative History. Cambridge: Cambridge University Press, 2010. ISBN 978-0-521-87818-0.

### `life-path-is-modern`

The name-and-birth-date 'life path' method is early-20th-century and American, originating with L. Dow Balliett.

- **[dudley1997]** (scholarly) Dudley, Underwood. Numerology: Or, What Pythagoras Wrought. Washington, DC: Mathematical Association of America, 1997.

### `notation-is-not-interpretation`

Representing quantity (numerical notation) and extracting meaning from letter values (gematria, isopsephy, numerology) are different activities and belong in different modules.

- **[chrisomalis2021]** (scholarly) Chrisomalis, Stephen. Reckonings: Numerals, Cognition, and History. Cambridge, MA: MIT Press, 2021.
- **[dudley1997]** (scholarly) Dudley, Underwood. Numerology: Or, What Pythagoras Wrought. Washington, DC: Mathematical Association of America, 1997.

### `pythagorean-label-is-borrowed`

The 'Pythagorean' label on modern numerology is borrowed. The method has no documented basis in the Pythagorean school.

- **[dudley1997]** (scholarly) Dudley, Underwood. Numerology: Or, What Pythagoras Wrought. Washington, DC: Mathematical Association of America, 1997.

### `readability-formulas-are-published`

Reading difficulty can be estimated by published formulas with named authors and dates. Readability is not cognitive load.

- **[flesch1948]** (scholarly) Flesch, Rudolf. 'A New Readability Yardstick.' Journal of Applied Psychology 32, no. 3 (1948): 221-33.
- **[kincaid1975]** (scholarly) Kincaid, J. Peter, Robert P. Fishburne, Richard L. Rogers and Brad S. Chissom. 'Derivation of New Readability Formulas for Navy Enlisted Personnel.' Naval Technical Training Command, Research Branch Report 8-75, 1975.

### `sexagesimal-positional`

Mesopotamian notation is positional, base 60, with a sub-base of 10 inside each digit, and no true zero sign.

- **[chrisomalis2010]** (scholarly) Chrisomalis, Stephen. Numerical Notation: A Comparative History. Cambridge: Cambridge University Press, 2010. ISBN 978-0-521-87818-0.

### `sexagesimal-primary-material`

The primary cuneiform material is held chiefly in the British Museum, the Louvre and Berlin.

- **[britishmuseum]** (collection) The British Museum, London. Mesopotamian collection.
- **[louvre]** (collection) Musee du Louvre, Paris. Near Eastern Antiquities.
- **[vorderasiatisches]** (collection) Vorderasiatisches Museum (Pergamonmuseum), Staatliche Museen zu Berlin.

### `vedic-attribution-unsupported`

The 'Vedic' attribution for planetary numerology is unsupported in the scholarly record. This is a gap in the evidence, not a demonstrated forgery.

- **[plofker2009]** (scholarly) Plofker, Kim. Mathematics in India. Princeton: Princeton University Press, 2009.
- **[murthy2005]** (scholarly) Murthy, S. S. N. 'Number Symbolism in the Vedas.' Electronic Journal of Vedic Studies 12, no. 3 (2005).

## Register

```text
[britishmuseum] (collection)
    The British Museum, London. Mesopotamian collection.
    Holds cuneiform mathematical tablets. Following the mid-19th-century Mesopotamian excavations, the bulk of this material came to rest in the British Museum, the Louvre and Berlin, and in university collections.

[chrisomalis2010] (scholarly)
    Chrisomalis, Stephen. Numerical Notation: A Comparative History. Cambridge: Cambridge University Press, 2010. ISBN 978-0-521-87818-0.
    Surveys more than 100 attested numerical notation systems across roughly 5,500 years. Originated as the author's PhD thesis at McGill University; the author is at Wayne State University. This is the standard comparative reference for every system in this package.

[chrisomalis2021] (scholarly)
    Chrisomalis, Stephen. Reckonings: Numerals, Cognition, and History. Cambridge, MA: MIT Press, 2021.
    Cognitive and historical analysis of numeral systems.

[dudley1997] (scholarly)
    Dudley, Underwood. Numerology: Or, What Pythagoras Wrought. Washington, DC: Mathematical Association of America, 1997.
    A mathematician's history and critique of numerology. The source for the finding that the modern name-and-birth-date method has no documented basis in the Pythagorean school, and for L. Dow Balliett's role in originating it.

[flesch1948] (scholarly)
    Flesch, Rudolf. 'A New Readability Yardstick.' Journal of Applied Psychology 32, no. 3 (1948): 221-33.
    Origin of the Reading Ease formula implemented here.

[iranica-chronograms] (reference)
    'Chronograms' (madda tarikh). Encyclopaedia Iranica. https://www.iranicaonline.org/
    Documents the Persian chronogram tradition: early poets wrote years out in words; later poets used abjad letter values, and from around the turn of the 14th century organised those values into meaningful words and phrases, a technique called hisab al-jummal. Mas'ud-e Sa'd-e Salman (d. 1121) is an attested early example.

[kincaid1975] (scholarly)
    Kincaid, J. Peter, Robert P. Fishburne, Richard L. Rogers and Brad S. Chissom. 'Derivation of New Readability Formulas for Navy Enlisted Personnel.' Naval Technical Training Command, Research Branch Report 8-75, 1975.
    Origin of the Flesch-Kincaid Grade Level formula.

[louvre] (collection)
    Musee du Louvre, Paris. Near Eastern Antiquities.
    Holds Mesopotamian primary material, including tablets.

[murthy2005] (scholarly)
    Murthy, S. S. N. 'Number Symbolism in the Vedas.' Electronic Journal of Vedic Studies 12, no. 3 (2005).
    Examines number symbolism in the Vedic corpus. States that the extent of Vedic influence on modern numerology is not known -- a gap in the record, which is why this library treats the 'Vedic numerology' label as unsupported rather than as disproven.

[plofker2009] (scholarly)
    Plofker, Kim. Mathematics in India. Princeton: Princeton University Press, 2009.
    The standard history of Indian mathematics. Cited here for the documented record of Indian numeration, and as the scholarly counterweight to systems marketed as 'Vedic' whose content does not appear in the Vedic corpus.

[unicode] (reference)
    The Unicode Standard. Unicode Consortium. https://www.unicode.org/versions/latest/
    Normative source for the code points of the three Greek numeral-only letters -- stigma (U+03DB), koppa (U+03DF) and sampi (U+03E1) -- and of their archaic alphabetic forms.

[vorderasiatisches] (collection)
    Vorderasiatisches Museum (Pergamonmuseum), Staatliche Museen zu Berlin.
    Holds one of the major cuneiform collections.
```
