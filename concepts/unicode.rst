=======
Unicode
=======

Some parts of Xapian treat strings as opaque blobs of data.  Here you can
put in any data you like (it can even contain zero bytes, at least at the
C++ level - whether zero bytes can be used in other languages mostly depends
whether the language allows them in strings).

There are places where Xapian needs to know the encoding of textual data
though - for example when stemming, in :xapian-class:`QueryParser` and
:xapian-class:`TermGenerator`, in :xapian-method:`MSet::snippet()`, etc.
In these places, the C++ API needs UTF-8 to be used.

Xapian contains Unicode data tables which are used for character
categorisation.  These get updated to the latest Unicode version for
each release series and then left at the same version for that release
series.  This avoids problems which can arise from using different Unicode
versions at index and search time due to different characters being treated
as part of a word.

---------------------
Unicode Normalisation
---------------------

Some characters can be represented in multiple ways in Unicode.  For example,
Å (U+00C5: "LATIN CAPITAL LETTER A WITH RING ABOVE"), Å (U+212B: "ANGSTROM SIGN") and A ̊ (U+0041: "LATIN CAPITAL LETTER A" + U+030A "COMBINING RING ABOVE") are defined by Unicode as "canonically equivalent".  A search system
should treat these as equivalent.

Unicode defines some normalised forms.  Xapian currently assumes data has been
converted to NFC ("Normalization Form C").  Here "C" stands for "Composition",
as this form generally used codepoints with precomposed accents in preference.

The `<https://www.macchiato.com/unicode-intl-sw/nfc-faq#h.h8uqckv6osay> NFC
FAQ`_ says:

    For example, according to data at Google: ~99.98% of web HTML page content
    characters are definitely NFC.

This data from 2009, and may vary in other use cases but it seems NFC is very
dominant in real-world use.

NFKC can also be used.  The difference is that NFKC is a lossy conversion.  It
includes some things which can be helpful (for example, NFKC also normalises
ligatures so ﬃ  (U+FB03) is converted to the 3 individual letters "ffi" and "oﬃ
ce" will match "office") but also some things which may be unhelpful (e.g. ²
(U+00B2) is normalised to "2", so "4²" would match "42").
