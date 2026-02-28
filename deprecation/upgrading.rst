=================================
Upgrading between Xapian versions
=================================

.. contents:: Table of contents

Introduction
============

.. FIXME: There's some overlap between this and deprecation.rst - I think some
   refactoring would be useful but I'm avoiding getting sidetracked into doing
   that right now in the interests of actually getting this section written
   before 2.0.0.

This section will guide you through the process of updating your code to work
with a new Xapian version.  We try to minimise incompatible changes between
versions, but occasionally they are necessary.

Xapian 2.x
==========

Deprecated features
-------------------

Features which were deprecated in 1.4.0 (or before) have been removed in 2.x -
if your code is still using them you'll need to update it.  See the section
on deprecated features below for a list of the deprecations, along with the
recommended replacements.

Usually features will be marked as deprecated for at least a full release cycle
before being removed, but there's an exception to this policy:

* :xapian-class:`LMWeight`: This class in 1.4.x was using incorrect formulae
  for all the smoothing schemes but this wasn't feasible to fix in 1.4.x so
  once we discovered it we advised users not to use this class (it's not the
  default weighting scheme and we don't believe it's been used much).  In 2.0.0
  this class was removed and replaced with a new separate class for each
  normalisation (except that Dirichlet and Dir+ are combined into one class):
  :xapian-class:`LM2StageWeight`, :xapian-class:`LMAbsDiscountWeight`,
  :xapian-class:`LMDirichletWeight` and :xapian-class:`LMJMWeight`.

Database API
------------

:xapian-class:`Database` and :xapian-class:`WritableDatabase` objects are now
reference counted handles like most other API classes and so are very cheap to
copy and assign; previously they were like vector<shard> which made copying and assignment O(#shards).

The main observable difference is that if you add a shard to a copy of a
:xapian-class:`Database` or :xapian-class:`WritableDatabase`, it's now added to
the original (which is consistent with other API classes, e.g. adding a
document to an :xapian-class:`RSet`).

Internal details
----------------

Some parts of the C++ API are marked as "internal" but have `public` visibility
for technical reasons.  You shouldn't rely on such internal details, and user
code using them may stop working without warning (potentially even in a point
release).

One specific case seen with the migration to Xapian 2.x was this code checking
if the database contains any shards:

.. code-block:: c++

  return !m_database.internal.empty();

This particular case can be done using public API since 1.4.12:

.. code-block:: c++

  return m_database.size() != 0;

More generally, if you find there's something you would need to use internal
API details to achieve, please tell us what you're trying to do and we can look
at adding a public API to support it.

std::string_view
----------------

Many places in the C++ API now take ``std::string_view`` parameters instead
of ``std::string`` or `const std::string&``.  This allows passing string
data which isn't already in a ``std::string`` without copying.

In rare cases, these means code which worked with 1.4.x can fail to compile
with 2.x.  We'll discuss some examples which illustrate the known causes
of this.

Implicit conversion to std::string
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

C++ code which relies to an implicit conversion to ``std::string`` may no
longer compile, for example this code compiles with 1.4.x:

.. code-block:: c++

    struct ImplicitString {
        operator std::string() { return std::string("term"); }
    };
    Xapian::Document doc;
    doc.add_term(ImplicitString());

However with 2.x, GCC gives compile error:

.. code-block:: text

    error: cannot convert ‘ImplicitString’ to ‘std::string_view’ {aka ‘std::basic_string_view<char>’}

If feasible, adding a conversion to ``std::string_view`` can fix this (and
may eliminate a copy):

.. code-block:: c++

    struct ImplicitString {
        operator std::string() { return std::string("term"); }
        operator std::string_view() { return std::string_view("term"); }
    };
    Xapian::Document doc;
    doc.add_term(ImplicitString());

Alternatively, you can make the conversion to ``std::string`` explicit:

.. code-block:: c++

    struct ImplicitString {
        operator std::string() { return std::string("term"); }
    };
    Xapian::Document doc;
    doc.add_term(std::string(ImplicitString()));

Both approaches will still work with 1.4.x (though the first requires that the
code is built as C++17 or newer).

Passing NULL/nullptr
~~~~~~~~~~~~~~~~~~~~

In C++, passing `NULL` or `nullptr` for a ``std::string_view`` parameter
fails to compile, but equivalent code for a ``const std::string&`` parameter
compiles.  Such code will fail if actually executed (it invokes undefined
behaviour, and will typically result in a segmentation fault), but an example
was seen in the wild in code which would never normally be executed.

Assuming an empty string is appropriate should the code be executed, passing
``""`` instead will compile with both 1.4.x and 2.x, and not crash if executed.

Database compatibility
----------------------

The glass database format is unchanged from 1.4.x, but there are potential
incompatibilities with how text is indexed which are detailed here.  In
some cases these may not be problematic, but in others you may decide they
warrant recreating your database from the source data.

Chert databases are no longer supported.  It's possible to convert a chert
database to glass - the same potential incompatibilities are relevant to
such a converted database.

Unicode Version
~~~~~~~~~~~~~~~

Xapian 2.0.0 upgraded to using Unicode 17.0.0 (1.4.x used Unicode 9.0.0)
which means Xapian now knows about 9983 additional assigned codepoints.
Also a very small number of codepoints have changed category.  Handling
of text containing affected codepoints will be different, but 1.4.x is
likely to not usefully index such text anyway.

You should consider reindexing if you're working with text written in scripts
which have new or improved support since Unicode 9.0.0.

Word tokenisation
~~~~~~~~~~~~~~~~~

Word tokenisation happens in :xapian-class:`TermGenerator` when indexing, in
:xapian-class:`QueryParser` when searching, and in
:xapian-method:`MSet::snippet()` when generating snippets for search results.
These all use the same definition of a word.

Two characters are always handled differently by 2.x:

- Unicode character U+200B (ZERO WIDTH SPACE) is now treated as whitespace
  rather than an ignored infix character.  It's used to mark word breaks in
  languages without visible space between words so should result in a word
  break.  This character is probably unlikely to appear in typed query strings,
  though might appear if users paste text as a query string.  It's probably
  only relevant for languages written without word breaks.

- Unicode character U+00AD (SOFT HYPHEN) is now treated as an ignored infix
  character so no longer results in a word break.  There are two common uses
  of this character: one is to mark potential hyphenation points (which this
  change means we now handle better), the other is to mark hyphens which have
  been inserted into text that has been word-wrapped (where it will be
  followed by the end of the line, so we'll handle such cases as we did
  before).  This character is probably unlikely to appear in typed query
  strings, though might appear if users paste text as a query string.

There are also differences in 2.x if you're using flags
:xapian-constant:`FLAG_NGRAMS` or :xapian-constant:`SNIPPET_NGRAMS` (older
names :xapian-constant:`FLAG_CJK_NGRAM` and
:xapian-constant:`SNIPPET_CJK_NGRAM`) as the list of codepoints for which
ngram terms are generated has been expanded to cover more some additional
scripts: Thai, Lana Tai, Pali, Lao, Myanmar (Burmese), Hangul, Khmer.  Also
relevant codepoints added between Unicode 9.0.0 and 17.0.0 are now included.

If you're working with text in one of these scripts, you may want to reindex.

You should also consider switching to the new
:xapian-constant:`FLAG_WORD_BREAKS` and :xapian-constant:`SNIPPET_WORD_BREAKS`
flags which use ICU's support for finding word boundaries.  These require
building xapian-core with support for ICU enabled.

Stemming
~~~~~~~~

Xapian 2.0.0 includes new stemming algorithms for some languages.  If you
are working with one of these languages you may want to enable stemming
for it and reindex:

* Esperanto
* Estonian
* Greek
* Hindi
* Nepali
* Polish
* Serbian
* Yiddish

Some stemmers are functionally identical in 1.4.x and 2.x:

* Armenian
* Basque
* Catalan
* Hungarian
* Indonesian
* Irish
* Lovins
* Porter
* Tamil

Some of the existing stemming algorithms have been improved, but this
means some words have different stems in Xapian 2.x.  If you have indexed text
with stemming using Xapian 1.4.x and search it with Xapian 2.x then the
stem produced for such a word at search time won't match that in the index.

While it might seem this would completely break search for affected words,
the effects can actually be more subtle and in some cases can even arguably
improve search results compared to 1.4.x.

For example, in 1.4.x the English stemmer stems *egged* and *egging* to *eg*,
which not only fails to conflate them with *egg* but also instead conflates
them with a relatively common abbreviation (meaning "for example").  2.0.0
addresses this - now *egged* and *egging* stem to *egg*.  If you search a 1.4.x
database using 2.x with English stemming, a search for *egged* won't match
*egged* or *egging* in the text, but it will now match *egg* in the text which
is likely to return some relevant results whereas with 1.4.x the same query
would have matched any document containing *egged* or *egging*, but also any
document containing *eg* which would likely have resulted in poor quality
results.

So for this case the stemming change is probably better without reindexing,
though using Xapian 2.x for both indexing and searching should work best
of all.

In general, reindexing with 2.x should give the best results but reindexing can
take significant time and resources for a large dataset so there's a trade-off.
The following stemmers have change stemming of some inputs - we'll analyse the
impact of the changes for each and summarise how worthwhile reindexing is
likely to be for each.

- Arabic: Punctuation marks are no longer removed by the stemmer - with
  Xapian such characters typically won't appear in the text passed to the
  stemmer anyway: if you're using the standard :xapian-class:`TermGenerator`
  and :xapian-class:`QueryParser` classes then stemming should be the same
  with both versions.

- Danish: This algorithm has been adjusted to prevent it mangling some "words"
  which are alphanumeric codes ending with two or more digits.  Searches which
  don't involve such codes are unaffected, while searching a database indexed
  with 1.4.x for affected codes won't work well with either version.

- Dutch: The stemmer name "dutch" now selects the Kraaij-Pohlmann algorithm
  instead of Martin Porter's Dutch stemmer as feedback from Dutch Snowball
  users was strongly that it does a better job.  Martin Porter's Dutch
  stemmer is now available as "dutch_porter".

  The "dutch" stemmer in 2.x stems many words differently to the "dutch"
  stemmer in 1.4.x - 20655 out of our sample vocabulary of 45670 words
  (45%).  Particularly notable is that the old algorithm undoubles vowels
  (so *maan* and *manen* stem to *man*) which the new algorithm doubles
  vowels (so *maan* and *manen* stem to *maan*).

  Reindexing is strongly recommended.  If not possible, we would suggest
  using the 2.x "dutch_porter" stemmer to search databases indexed using the
  1.4.x "dutch" stemmer (which should give identical stems for all Dutch
  words (see below for full details).

- Dutch (Kraaij-Pohlmann): This is the "kraaij_pohlmann" in 1.4.x and 2.x
  (it's also now the "dutch" stemmer in 2.x).  The version in 2.x has been
  fixed to match the behaviour of the original C implementation, which changed
  the stems for 220 words out of our sample vocabulary of 45670 words, and
  then a small number of exceptions were added to address cases which Martin
  Porter's Dutch stemmer handled better, which changed the stems of a further
  21 words for a total of 241 (0.53%).  Some of these will still return
  reasonable results but reindexing is probably worthwhile if easy to do.

- Dutch (Porter): This was the "dutch" stemmer in 1.4.x and is the
  "dutch_porter" stemmer in 2.x.  The only change is to fix the setting up
  of R1 where "at least 3 characters" was actually implemented as "at least
  3 bytes".  This doesn't affect any words in our sample vocabulary.  We strip
  accents normally found in Dutch except for `è` before setting R1, and no
  Dutch words starting `è` seem to stem differently after this change, but
  proper nouns and other words of foreign origin may be affected.

  There's not a compelling reason to reindex due to this change, but
  reindexing allows switching to the new "dutch" stemmer in 2.x which
  reportedly does a significantly better job.

- Early English: The "earlyenglish" stemmer is now based on the "english"
  stemmer instead of "porter".  Testing on our sample modern English vocabulary
  of 42649 words, 2299 words are stemmed differently (5.4%).  If you're using
  this stemmer then reindexing is recommended.

- English: Various cases reported by users have been improved, and 57 words
  out of our 42649 word sample vocabulary now stem different (0.13%).  In some
  cases (such as the *egging* example noted above) searching a 1.4.x database
  with Xapian 2.x will probably be no worse and perhaps better than searching
  with 1.4.x, though reindexing and searching with 2.x will give better
  results for this small subset of searches.  There's not a compelling need to
  reindex, but if it's easy to do it is worth considering.

- Finnish: This algorithm has been adjusted to prevent it truncating some
  numbers.  Stemming of Finnish words is unchanged, but some foreign words
  containing accented characters not used in Finnish are no longer modified
  by the algorithm (this affects 3 non-Finnish words in our 49962 word sample
  vocabulary).  Searching a database indexed with 1.4.x for affected numbers
  won't work well with either version; searches for affected foreign words will
  probably work less well with mixed versions.

- French: Various cases reported by users have been improved, and 919 words
  out of our 21642 word sample vocabulary (4.2%) are stemmed differently by
  2.x.  Of these, 801 of the 919 are affected by a change to remove elisions
  (e.g.  *l'état* now stems to *état*), and a search for one of these with 2.x
  against a 1.4.x database for one of these will at least match uses of the
  word without an elision in documents.  Many cases will still return
  reasonable results, but reindexing is recommended if easy to do.

- German: Various cases reported by users have been improved, but also the
  "german2" variant which normalises umlauts ("ä" to "ae", "ö" to "oe", "ü" to
  "ue") has been merged into the main algorithm.  1247 words out of our
  35033 word sample vocabulary (3.6%) now stem differently.  Many cases will
  still return reasonable results, but reindexing is recommended if easy to do.

- Italian: The stem of *divano* (sofa) is now *divan* (which matches the stem
  of its plural form *divani*).  Previously it was stemmed to *div* which
  conflated it with *diva* (diva).  No other words are affected, and even
  searches for *divano* with 2.x against a 1.4.x database will now match
  *divani* in documents so there's no compelling reason to reindex.

- Lithuanian: The stemming of 156 words out of our sample vocabulary of 86105
  words has changed (0.18%).  This improves some cases where the forms of a
  particular word stemmed to one of two different stems but now stem to a
  single stem, and searches for affected words will still match some forms
  of that word in documents so should return reasonable results.  There's not a
  compelling need to reindex, but if it's easy to do it is worth considering.

- Norwegian: Two cases reported by users have been improved, and 136 words
  out of our sample vocabulary of 20895 words now stem differently (0.65%).
  In most of the affected cases, the forms of a particular word stemmed to one
  of two different stems before but now stem to a single stem, and searches for
  affected words will still match some forms of that word in documents so
  should return reasonable results.  There's not a compelling need to reindex,
  but if it's easy to do it is worth considering.

- Portuguese: The stemmer incorrectly included some Spanish suffixes which have
  been replaced by the intended Portuguese suffixes, which changes the stemming
  of 10 words out of our sample vocabulary of 32016 words (0.03%).  In most of
  the affected cases, the new stem matches the existing stem of other forms of
  the word, so searches for affected words will still match some forms of that
  word in documents and should return reasonable results.  There's not a
  compelling need to reindex, but if it's easy to do it is worth considering.

- Romanian: Romanian uses characters *ş* and *ţ* - the accent here is
  "comma-under" but before full Unicode support was widespread it was common
  to use the similar looking "cedilla" accented forms instead.  The 1.4.x
  version of the stemmer only handled the cedilla forms, but the 2.x version
  handles both the cedilla and comma-under forms by mapping comma-under to
  cedilla as a new initial step.  This changes the stems of 13249 words out
  of our sample vocabulary of 87642 words (15.1%).  Searches which don't
  feature these accented characters will work as before, and some cases will
  still match related forms, but given the proportion of words affected and
  the improvement of stemming for modern Unicode text, reindexing is
  recommended.

- Russian: The stemmer now normalises *ё* to *e* before stemming, which changes
  the stems of 112 words out of our sample vocabulary of 49785 words (0.2%).
  There's not a compelling need to reindex, but if it's easy to do it is worth
  considering.

- Spanish: The stemmer now handles some common cases of suffixes with missing
  accents: *-acion* like *-ación* and *-ucion* like *-ución*.  This changes
  the stems of 9 words out of our sample vocabulary of 28378 words (0.03%).
  Depending on the dataset being indexed, missing accents may be more common
  in queries than documents, in which case searching a 1.4.x database using 2.x
  may give better results than searching with 1.4.x.  There's not a compelling
  need to reindex, but if it's easy to do it is worth considering.

- Swedish: Two cases reported by users have been improved, and 553 words
  out of our sample vocabulary of 30738 words now stem differently (1.8%).
  In most of the affected cases, the new stem matches the stem of other forms
  of the same word, so searches for affected words will still match some forms
  of that word in documents and should return reasonable results.  There's not
  a compelling need to reindex, but if it's easy to do it is worth considering.

- Turkish: Proper noun suffixes are now removed - for example, *Türkiye'dir*
  ("it is Turkey") is now conflated with *Türkiye* ("Turkey").  This
  changes the stems of 9204 words out of our sample vocabulary of 96325 words
  (9.6%).  This will only affect searching a 1.4.x database with 2.x for
  queries containing a suffixed proper noun, and such queries will still match
  documents where that proper noun appears unsuffixed so should return
  reasonable results in many cases, but reindexing is probably worthwhile if
  easy to do.
