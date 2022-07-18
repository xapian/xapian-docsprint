=====================
Python Specific Notes
=====================

The Python3 bindings for Xapian are packaged in the ``xapian`` module,
so to use them you need to add this to your code::

  import xapian

They require Python >= 3.2 in Xapian 1.4.x.

The Python API largely follows the C++ API - the differences and
additions are noted below.

Strings
=======

The Xapian C++ API is largely agnostic about character encoding, and uses the
`std::string` type as an opaque container for a sequence of bytes.
In places where the bytes represent text (for example, in the
`Stem`, `QueryParser` and `TermGenerator` classes), UTF-8 encoding is used.  In
order to wrap this for Python, `std::string` is mapped to/from the Python
`bytes` type.

As a convenience, you can also pass Python
`str` objects as parameters where this is appropriate, which will be
converted to UTF-8 encoded text.  Where `std::string` is
returned, it's always mapped to `bytes` in Python, which you can
convert to a Python `str` by calling `.decode('utf-8')`
on it like so::

  for i in doc.termlist():
    print(i.term.decode('utf-8'))

Unicode
#######

The xapian Python bindings accept unicode strings as well as simple strings
(ie, "str" type strings) at all places in the API which accept string data.
Any unicode strings supplied will automatically be translated into UTF-8
simple strings before being passed to the Xapian core.  The Xapian core is
largely agnostic about character encoding, but in those places where it does
process data in a character encoding dependent way it assumes that the data
is in UTF-8.  The Xapian Python bindings always return string data as simple
strings.

Therefore, in order to avoid issues with character encodings, you should
always pass text data to Xapian as unicode strings, or UTF-8 encoded simple
strings.  There is, however, no requirement for simple strings passed into
Xapian to be valid UTF-8 encoded strings, unless they are being passed to a
text processing routine (such as the query parser, or the stemming
algorithms).  For example, it is perfectly valid to pass arbitrary binary
data in a simple string to the ``xapian.Document.set_data()``
method.

It is often useful to normalise unicode data before passing it to Xapian -
Xapian currently has no built-in support for normalising unicode
representations of data.  The standard python module
"``unicodedata``" provides support for normalising unicode: you
probably want the "``NFKC``" normalisation scheme: in other words,
use something like

::

  unicodedata.normalize('NFKC', u'foo')

to normalise the string "foo" before passing it to Xapian.


Exceptions
##########

Xapian-specific exceptions are subclasses of the :xapian-class:`Error`
class, so you can trap all Xapian-specific exceptions like so::

    try:
        do_something_with_xapian()
    except xapian.Error as e:
        print str(e)

:xapian-class:`Error` is itself a subclass of the standard Python
`exceptions.Exception` class.

Iterators
#########

The iterator classes in the Xapian C++ API are wrapped in a pythonic style.
The following are supported (where marked as "default iterator", it means
``__iter__()`` does the right
thing so you can for instance use ``for term in document`` to
iterate over terms in a Document object):


+----------------------+------------------------------------------+---------------------------------------+----------------------+
| Class                | Python Method                            | Equivalent C++ Method                 | Python iterator type |
+======================+==========================================+=======================================+======================+
|``MSet``              | default iterator                         | ``begin()``                           | ``MSetIter``         |
+----------------------+------------------------------------------+---------------------------------------+----------------------+
|``ESet``              | default iterator                         | ``begin()``                           | ``ESetIter``         |
+----------------------+------------------------------------------+---------------------------------------+----------------------+
|``Enquire``           | ``matching_terms()``                     | ``get_matching_terms_begin()``        | ``TermIter``         |
+----------------------+------------------------------------------+---------------------------------------+----------------------+
|``Query``             | default iterator                         | ``get_terms_begin()``                 | ``TermIter``         |
+----------------------+------------------------------------------+---------------------------------------+----------------------+
|``Database``          | ``allterms()`` (also as default iterator)| ``allterms_begin()``                  | ``TermIter``         |
+----------------------+------------------------------------------+---------------------------------------+----------------------+
|``Database``          | ``postlist(tname)``                      | ``postlist_begin(tname)``             | ``PostingIter``      |
+----------------------+------------------------------------------+---------------------------------------+----------------------+
|``Database``          | ``termlist(docid)``                      | ``termlist_begin(docid)``             | ``TermIter``         |
+----------------------+------------------------------------------+---------------------------------------+----------------------+
|``Database``          | ``positionlist(docid, tname)``           | ``positionlist_begin(docid, tname)``  | ``PositionIter``     |
+----------------------+------------------------------------------+---------------------------------------+----------------------+
|``Database``          | ``metadata_keys(prefix)``                | ``metadata_keys(prefix)``             | ``TermIter``         |
+----------------------+------------------------------------------+---------------------------------------+----------------------+
|``Database``          | ``spellings()``                          | ``spellings_begin(term)``             | ``TermIter``         |
+----------------------+------------------------------------------+---------------------------------------+----------------------+
|``Database``          | ``synonyms(term)``                       | ``synonyms_begin(term)``              | ``TermIter``         |
+----------------------+------------------------------------------+---------------------------------------+----------------------+
|``Database``          | ``synonym_keys(prefix)``                 | ``synonym_keys_begin(prefix)``        | ``TermIter``         |
+----------------------+------------------------------------------+---------------------------------------+----------------------+
|``Document``          | ``values()``                             | ``values_begin()``                    | ``ValueIter``        |
+----------------------+------------------------------------------+---------------------------------------+----------------------+
|``Document``          | ``termlist()`` (also as default iterator)| ``termlist_begin()``                  | ``TermIter``         |
+----------------------+------------------------------------------+---------------------------------------+----------------------+
|``QueryParser``       | ``stoplist()``                           | ``stoplist_begin()``                  | ``TermIter``         |
+----------------------+------------------------------------------+---------------------------------------+----------------------+
|``QueryParser``       | ``unstemlist(tname)``                    | ``unstem_begin(tname)``               | ``TermIter``         |
+----------------------+------------------------------------------+---------------------------------------+----------------------+
|``ValueCountMatchSpy``|  ``values()``                            | ``values_begin()``                    | ``TermIter``         |
+----------------------+------------------------------------------+---------------------------------------+----------------------+
|``ValueCountMatchSpy``|  ``top_values()``                        | ``top_values_begin()``                | ``TermIter``         |
+----------------------+------------------------------------------+---------------------------------------+----------------------+


The pythonic iterators generally return Python objects, with properties
available as attribute values, with lazy evaluation where appropriate.  An
exception is the ``PositionIter`` object returned by
``Database.positionlist``, which returns an integer.

The lazy evaluation is mainly transparent, but does become visible in one
situation: if you keep an object returned by an iterator, without evaluating
its properties to force the lazy evaluation to happen, and then move the
iterator forward, the object may no longer be able to efficiently perform the
lazy evaluation.  In this situation, an exception will be raised indicating
that the information requested wasn't available.  This will only happen for a
few of the properties - most are either not evaluated lazily (because the
underlying Xapian implementation doesn't evaluate them lazily, so there's no
advantage in lazy evaluation), or can be accessed even after the iterator has
moved.  The simplest work around is simply to evaluate any properties you wish
to use which are affected by this before moving the iterator.  The complete set
of iterator properties affected by this is:

- Database.allterms (also accessible as Database.__iter__): **termfreq**
- Database.termlist: **termfreq** and **positer**
- Document.termlist (also accessible as Document.__iter__): **termfreq** and **positer**
- Database.postlist: **positer**

MSet
####

MSet objects have some additional methods to simplify access (these
work using the C++ array dereferencing):

+------------------------------------+----------------------------------------+
| Method name                        |            Explanation                 |
+====================================+========================================+
| ``get_hit(index)``                 |  returns MSetItem at index             |
+------------------------------------+----------------------------------------+
| ``get_document_percentage(index)`` | ``convert_to_percent(get_hit(index))`` |
+------------------------------------+----------------------------------------+
| ``get_document(index)``            | ``get_hit(index).get_document()``      |
+------------------------------------+----------------------------------------+
| ``get_docid(index)``               | ``get_hit(index).get_docid()``         |
+------------------------------------+----------------------------------------+

Additionally, the MSet has a property, ``mset.items``, which returns a
list of tuples representing the MSet.  This is now deprecated - please use the
property API instead (it works in Xapian 1.0.x too).  The tuple members and the
equivalent property names are as follows:


+-------------------------+---------------+---------------------------------------------------------------------------+
|   Index                 | Property name | Contents                                                                  |
+=========================+===============+===========================================================================+
| ``xapian.MSET_DID``     | docid         | Document id                                                               |
+-------------------------+---------------+---------------------------------------------------------------------------+
| ``xapian.MSET_WT``      | weight        |  Weight                                                                   |
+-------------------------+---------------+---------------------------------------------------------------------------+
| ``xapian.MSET_RANK``    | rank          | Rank                                                                      |
+-------------------------+---------------+---------------------------------------------------------------------------+
| ``xapian.MSET_PERCENT`` |  percent      | Percentage weight                                                         |
+-------------------------+---------------+---------------------------------------------------------------------------+
| ``xapian.MSET_DOCUMENT``| document      | Document object (Note: this member of the tuple was never actually set!)  |
+-------------------------+---------------+---------------------------------------------------------------------------+


Two MSet objects are equal if they have the same number and maximum possible
number of members, and if every document member of the first MSet exists at the
same index in the second MSet, with the same weight.

Non-Class Functions
###################

The C++ API contains a few non-class functions (the Database factory
functions, and some functions reporting version information), which are
wrapped like so for Python 3:

- ``Xapian::version_string()`` is wrapped as ``xapian.version_string()``
- ``Xapian::major_version()`` is wrapped as ``xapian.major_version()``
- ``Xapian::minor_version()`` is wrapped as ``xapian.minor_version()``
- ``Xapian::revision()`` is wrapped as ``xapian.revision()``
- ``Xapian::Remote::open()`` is wrapped as ``xapian.remote_open()`` (both the TCP and "program" versions are wrapped - the SWIG wrapper checks the parameter list to decide which to call).
- ``Xapian::Remote::open_writable()`` is wrapped as ``xapian.remote_open_writable()`` (both the TCP and "program" versions are wrapped - the SWIG wrapper checks the parameter list to decide which to call).

The version of the bindings in use is available as `xapian.__version__` (as
recommended by PEP 396).  This may not be the same as `xapian.version_string()`
as the latter is the version of xapian-core (the C++ library) in use.

Query
#####

In C++ there's a Xapian::Query constructor which takes a query operator and
start/end iterators specifying a number of terms or queries, plus an optional
parameter.  In Python, this is wrapped to accept any Python sequence (for
example a list or tuple) to give the terms/queries, and you can specify
a mixture of terms and queries if you wish.  For example:


::

  subq = xapian.Query(xapian.Query.OP_AND, "hello", "world")
  q = xapian.Query(xapian.Query.OP_AND, [subq, "foo", xapian.Query("bar", 2)])


MatchAll and MatchNothing
-------------------------

As of 1.1.1, these are wrapped as ``xapian.Query.MatchAll`` and
``xapian.Query.MatchNothing``.


MatchDecider
############

Custom MatchDeciders can be created in Python - subclass
``xapian.MatchDecider``, ensure you call the super-constructor, and define a
``__call__`` method that will do the work. The simplest example (which does nothing
useful) would be as follows:

::

  class mymatchdecider(xapian.MatchDecider):
    def __init__(self):
      xapian.MatchDecider.__init__(self)

    def __call__(self, doc):
      # Accept all documents.
      return True


RangeProcessors
###############

The ``RangeProcessor`` class (and its subclasses) provide an ``operator()``
method in C++ which is exposed in Python as a ``__call__()`` method, making the
class instances into callables.

This method checks whether a beginning and end of a range are in a format
understood by the ``RangeProcessor``, and if so returns a ``Query`` object
which matches the range (typically it converts the beginning and end into
strings which sort appropriately and returns an ``OP_VALUE_RANGE`` query).
There are several built-in ``RangeProcessor`` subclasses, but you can also
define custom ones in python.

::

  class MyRP(xapian.RangeProcessor):
      def __init__(self):
          xapian.RangeProcessor.__init__(self)
      def __call__(self, begin, end):
          return xapian.Query(xapian.Query.OP_VALUE_RANGE, "A"+begin, "B"+end)

Apache and mod_python/mod_wsgi
##############################

Prior to Xapian 1.3.0, you had to tell mod_python and mod_wsgi to run
applications which use Xapian in the main interpreter.  Xapian 1.3.0 no
longer uses the simplified GIL state API, and so this restriction no
longer applies.
