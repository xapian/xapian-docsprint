.. Original content was taken from xapian-core/docs/serialisation.rst with
.. a copyright statement of:
.. Copyright (C) 2009 Lemur Consulting Ltd
.. Copyright (C) 2009 Olly Betts

======================================
Serialisation of Queries and Documents
======================================

.. contents:: Table of contents

Introduction
============

In order to pass :xapian-class:`Query` and :xapian-class:`Document` objects to
or from remote databases, Xapian includes support for serialising these objects
to binary strings, and then converting these strings back into objects.  This
support may be accessed directly, and used for storing persistent
representations of such objects.  The representations used are not architecture
dependent, so you can successfully unserialise an object on a machine with a
different word size or endianness to the machine it was serialised on.

Be aware that the serialised representation may change between release series,
so if you're using serialised objects for long term storage you will need a
strategy for dealing with this.  Changes to the representation will be clearly
noted in the release notes.

Serialising Documents
=====================

If you have a :xapian-class:`Document` object which you want to serialise,
you can call the :xapian-method:`Document::serialise()` method on it, which
returns a string.

Documents are often lazily fetched from databases: this method will first force
the full document contents to be fetched from the database, in order to
serialise them.  The serialised document will have identical contents (data,
terms, positions, values) to the original document.

To get a document from a serialised form, call the static
:xapian-method:`Document::unserialise()` method, passing it the string returned
from :xapian-just-method:`serialise()`, which will give you a new
:xapian-class:`Document` object.

Serialising Queries
===================

Serialisation of queries is very similar to serialisation of documents: there
is a :xapian-method:`Query::serialise()` method to produce a serialised Query,
and a corresponding :xapian-method:`Query::unserialise()` method to produce a
:xapian-class:`Query` object from a serialised representation.

However, there is a wrinkle.  A query can contain arbitrary user-defined
:xapian-class:`PostingSource` subqueries.  In order to serialise and
unserialise such queries, all the :xapian-class:`PostingSource` subclasses used
in the query must implement the :xapian-just-method:`name()`,
:xapian-just-method:`serialise()` and :xapian-just-method:`unserialise()`
methods (see :ref:`postingsource` for details).

In addition, a special form of unserialise must be used which takes a
:xapian-class:`Registry` object as an additional parameter, which must know
all the custom posting sources used in the query.  You need to call
:xapian-method:`Registry::register_posting_source()` to register each such
class.

Note that :xapian-class:`Registry` objects always know about built-in posting
sources (such as :xapian-class:`ValueWeightPostingSource`), so you don't need
to call :xapian-just-method:`register_posting_source()` for them.
