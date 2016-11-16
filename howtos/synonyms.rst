.. Original content was taken from xapian-core/docs/synonyms.rst with
.. a copyright statement of:
.. Copyright (C) 2007,2008,2011 Olly Betts

========
Synonyms
========

Introduction
============

Xapian provides support for storing a synonym dictionary, or thesaurus.  This
can be used by the :xapian-class:`QueryParser` class to expand terms in user query
strings, either automatically, or when requested by the user with an explicit
synonym operator (``~``).

.. note::
   Xapian doesn't offer automated generation of the synonym dictionary.

Here is an example of search program with synonym functionality.

.. xapianexample:: search_synonyms

You can see the search results without `~` operator.

.. xapianrunexample:: index1
    :silent:
    :args: data/100-objects-v1.csv db

.. xapianrunexample:: delete1
    :silent:
    :args: db 1953-448 1985-438

.. xapianrunexample:: search_synonyms
    :args: db time

Notice the difference with the `~` operator with `time` where `calendar` is specified as its synonym.

.. xapianrunexample:: index1
    :silent:
    :args: data/100-objects-v1.csv db

.. xapianrunexample:: delete1
    :silent:
    :args: db 1953-448 1985-438

.. xapianrunexample:: search_synonyms
    :args: db ~time

Model
=====

The model for the synonym dictionary is that a term or group of consecutive
terms can have one or more synonym terms.  A group of consecutive terms is
specified in the dictionary by simply joining them with a single space between
each one.

If a term to be synonym expanded will be stemmed by the :xapian-class:`QueryParser`, then
synonyms will be checked for the unstemmed form first, and then for the stemmed
form, so you can provide different synonyms for particular unstemmed forms
if you want to.

.. todo:: Discuss interactions with stemming (ie, should the input and/or output values in the synonym table be stemmed).

Adding Synonyms
===============

The synonyms can be added by the :xapian-method:`WritableDatabase::add_synonym()`. In the following 
example ``calender`` is specified as a synonym for ``time``. Users may similarly write a loop to load all
the synonyms from a dictionary file.

.. xapianexample:: search_synonyms
    :start-after: Start of adding synonyms
    :end-before: End of adding synonyms

QueryParser Integration
=======================

In order for any of the synonym features of the QueryParser to work, you must
call :xapian-method:`QueryParser::set_database()` to specify the database to
use.

.. xapianexample:: search_synonyms
    :start-after: Start of set database
    :end-before: End of set database

If ``FLAG_SYNONYM`` is passed to :xapian-method:`QueryParser::parse_query()`
then the :xapian-class:`QueryParser` will recognise ``~`` in front of a term as indicating a
request for synonym expansion.  

If ``FLAG_LOVEHATE`` is also specified, you can
use ``+`` and ``-`` before the ``~`` to indicate that you love or hate the
synonym expanded expression.

A synonym-expanded term becomes the term itself `OP_SYNONYM`-ed with any listed synonyms,
so ``~truck`` might expand to ``truck SYNONYM lorry SYNONYM van``.  A group of terms is
handled in much the same way.

If ``FLAG_AUTO_SYNONYMS`` is passed to
:xapian-method:`QueryParser::parse_query()` then the :xapian-class:` QueryParser` will
automatically expand any term which has synonyms, unless the term is in a phrase
or similar.

If ``FLAG_AUTO_MULTIWORD_SYNONYMS`` is passed to
:xapian-method:`QueryParser::parse_query()` then the :xapian-class:` QueryParser` will look at
groups of terms separated only by whitespace and try to expand them as term
groups.  This is done in a "greedy" fashion, so the first term which can start a
group is expanded first, and the longest group starting with that term is
expanded.  After expansion, the :xapian-class:` QueryParser` will look for further possible
expansions starting with the term after the last term in the expanded group.

OP_SYNONYM
==========

.. todo:: Query.OP_SYNONYM, and how that relates to synonym expansion.

Current Limitations
===================

Explicit multi-word synonyms
----------------------------

There ought to be a way to explicitly request expansion of multi-term synonyms,
probably with the syntax ``~"stock market"``.  This hasn't been implemented
yet though.

Backend Support
---------------

Currently synonyms are supported by the chert and glass databases.  They work
with a single database or multiple databases (use
:xapian-method:`Database::add_database()` as usual).  We've no plans to support
them for the InMemory backend, but we do intend to support them for the remote
backend in the future.
