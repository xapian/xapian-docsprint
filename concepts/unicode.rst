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
Å (U+00C5: "LATIN CAPITAL LETTER A WITH RING ABOVE"), Å (U+212B: "ANGSTROM
SIGN") and A ̊ (U+0041: "LATIN CAPITAL LETTER A" + U+030A "COMBINING RING
ABOVE") are defined by Unicode as "canonically equivalent".  A search query
using one representation should match a document using a different
representation.  In Xapian that's best achieved by normalising the
representation used in terms.

Unicode defines some normalised forms.  Xapian currently assumes data has been
converted to NFC ("Normalization Form C") or NFKC.  Here "C" stands for
"Composition", as this form generally uses codepoints with precomposed accents
in preference.

NFKC is similar to NFC - the difference is that some additional lossy
normalisation is done.  For example, NFKC normalises ligature codepoints such
as "ﬃ", (where the three letters are the single Unicode codepoint U+FB03) to
the three individual letters "ffi", so "oﬃce" will match "office".

Normalising ligatures is desirable if you are dealing with text containing them,
but some of the NFKC normalisations are less clearly desirable in the context of
search - for example, ² (U+00B2) is normalised to "2", so NFKC normalises "4²"
to "42", which seems unhelpful.  However note that if the superscript was
instead done via a font effect (e.g. `4<sup>2</sup>` in HTML) then this would
likely also result in the term "42", and the normalisation of related cases
such as "H₂SO₄" to "H2SO4" does seem useful.

The `<https://www.macchiato.com/unicode-intl-sw/nfc-faq#h.h8uqckv6osay> NFC
FAQ`_ says:

    For example, according to data at Google: ~99.98% of web HTML page content
    characters are definitely NFC.

This data is from 2009, and may vary in other use cases but it seems NFC is
very dominant in real-world use.  It's not clear if the cited report attempted
to discriminate NFKC from NFC (pages which are NFKC are a strict subset of
pages which are NFC) and we've not managed to locate the original source of
this statistic.
