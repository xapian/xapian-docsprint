.. Original content was taken from xapian-core/docs/postingsource.rst with
.. a copyright statement of:

.. Copyright (C) 2008,2009,2010,2011,2013 Olly Betts
.. Copyright (C) 2008,2009 Lemur Consulting Ltd

.. _postingsource:

===============
Posting sources
===============

.. contents:: Table of contents

Introduction
============

:xapian-class:`PostingSource` is an API class which you can subclass to
feed data to Xapian's matcher.  This feature can be made use of in a number of
ways - for example:

As a filter - a subclass could return a stream of document ids to filter a
query against.

As a weight boost - a subclass could return every document, but with a
varying weight so that certain documents receive a weight boost.  This could
be used to prefer documents based on some external factor, such as age,
price, proximity to a physical location, link analysis score, etc.

As an alternative way of ranking documents - if the weighting scheme is set
to :xapian-class:`BoolWeight`, then the ranking will be entirely by the weight
returned by :xapian-class:`PostingSource`.

Example
=======

.. todo:: clean up the example to better show what we're trying to do

:xapian-class:`ExternalWeightPostingSource` doesn't restrict which documents
match - it's intended to be combined with an existing query using
:xapian-just-constant:`OP_AND_MAYBE` like so::

    extwtps = xapian.ExternalWeightPostingSource(db, wtsource)
    query = xapian.Query(query.OP_AND_MAYBE, query, xapian.Query(extwtps))

The wtsource would be a class like this one::

    class WeightSource(object):
        def get_maxweight(self):
            return 12.34;

        def get_weight(self, doc):
            return some_func(doc.get_docid())

We'll work through an example of a :xapian-class:`PostingSource` which
contributes additional weight from some external source (note that in Python,
you call ``next()`` on an iterator to get each item, including the first, which
is exactly the semantics we need to implement here).

.. xapianexample:: postingsource
    :marker: class header and constructor

When first constructed, a :xapian-class:`PostingSource` is not tied to a
particular database.  Before Xapian can get any postings (or statistics) from
the source, it needs to be supplied with a database.  This is performed by the
:xapian-just-method:`init(db)` method, where :xapian-variable:`db` specifies
the database to use.  This method will always be called before asking for any
information about the postings in the list.  If a posting source is used for
multiple searches, the :xapian-just-method:`init()` method will be called
before each search; implementations must cope with :xapian-just-method:`init()`
being called multiple times, and should always use the database provided in the
most recent call.

Here we store the passed database, initialise an iterator to iterate over
the documents we want the :xapian-class:`PostingSource` to match, and tell
the base class what the maximum weight we can return is:

.. xapianexample:: postingsource
    :marker: init

If your :xapian-class:`PostingSource` class always returns 0 from
:xapian-just-method:`get_weight()`, then there's no need to call
:xapian-just-method:`set_maxweight()`.

If you are returning weights you should try hard to find a bound for
efficiency, but if there really isn't one then you can set
:xapian-literal:`DBL_MAX`.

This method specifies an upper bound on what :xapian-just-method:`get_weight()`
will return *from now on* (until the next call to
:xapian-just-method:`init()`).  So if you know that the upper bound has
decreased, you should call :xapian-just-method:`set_maxweight()` with the new
reduced bound.

One thing to be aware of is that currently calling
:xapian-just-method:`set_maxweight()` during the match triggers an recursion
through the postlist tree to recalculate the new overall maxweight, which takes
a comparable amount of time to calculating the weight for a matching document.
If your maxweight reduces for nearly every document, you may want to profile to
see if it's beneficial to notify every single change.  Experiments with a
modified :xapian-class:`FixedWeightPostingSource` which forces a pointless
recalculation for every document suggest a worst case overhead in search times
of about 37%, but reports of profiling results for real world examples are most
welcome.  In real cases, this overhead could easily be offset by the extra
scope for matcher optimisations which a tighter maxweight bound allows.

A simple approach to reducing the number of calculations is only to do it every
N documents.  If it's cheap to calculate the maxweight in your posting source,
a more sophisticated strategy might be to decide an absolute maximum number of
times to update the maxweight (say 100) and then to call it whenever::

    last_notified_maxweight - new_maxweight >= original_maxweight / 100.0

This ensures that only reasonably significant drops result in a recalculation
of the maxweight.

Since :xapian-just-method:`get_weight()` must always return >= 0, the upper
bound must clearly also always be >= 0 too.  If you don't call
:xapian-just-method:`get_maxweight()` then the bound defaults to 0, to match
the default implementation of :xapian-just-method:`get_weight()`.

If you want to read the currently set upper bound, you can call
:xapian-just-method:`get_maxweight()`.  This is just a getter method for a
member variable in the :xapian-class:`PostingSource` class, and is inlined from
the API headers, so there's no point storing this yourself in your subclass -
it should be just as efficient to call :xapian-just-method:`get_maxweight()`
whenever you want to use it.

Three methods return statistics independent of the iteration position.
These are upper and lower bounds for the number of documents which can
be returned, and an estimate of this number.  In this case, we know this
exactly, as it is just the number of documents in the database:

.. xapianexample:: postingsource
    :marker: termfreq methods

These methods aren't implemented in the base class, so you have to define them
when deriving your subclass.

It must always be true that
:xapian-method:`get_termfreq_min()` <= :xapian-method:`get_termfreq_est()` and
:xapian-method:`get_termfreq_est()` <= :xapian-method:`get_termfreq_max()`.

PostingSources must always return documents in increasing document ID order.

After construction, a PostingSource points to a position *before* the first
document id - so before a docid can be read, the position must be advanced
by calling :xapian-just-method:`next()`, :xapian-just-method:`skip_to()` or
:xapian-just-method:`check()`.

The :xapian-just-method:`get_weight()` method returns the weight that you want to contribute
to the current document.  This weight must always be >= 0:

.. xapianexample:: postingsource
    :marker: get_weight

The default implementation of :xapian-just-method:`get_weight()` returns 0, for
convenience when deriving "weight-less" subclasses.

The :xapian-just-method:`get_docid()` method returns the document id at the
current iteration position:

.. xapianexample:: postingsource
    :marker: get_docid

And the :xapian-just-method:`at_end()` method checks if the current iteration
position is past the last entry - we signal that in our subclass by setting
the current position to an invalid value:

.. xapianexample:: postingsource
    :marker: at_end

There are three methods which advance the current position.  All of these take
a parameter :xapian-variable:`min_wt`, which indicates the minimum weight
contribution which the matcher is interested in.  The matcher still checks the
weight of documents so it's OK to ignore this parameter completely, or to use
it to discard only some documents.  But it can be useful for optimising in some
cases.

The simplest of these three methods is :xapian-just-method:`next(min_wt)`,
which simply advances the iteration position to the next document (possibly
skipping documents with weight contribution < min_wt):

.. xapianexample:: postingsource
    :marker: next

Then there's :xapian-just-method:`skip_to(did, min_wt)`.  This advances the
iteration position to the next document with document id >= did, possibly also
skipping documents with weight contribution < min_wt.

.. xapianexample:: postingsource
    :marker: skip_to

A default implementation of :xapian-just-method:`skip_to()` is provided which
just calls :xapian-just-method:`next()` repeatedly.  This works but
:xapian-just-method:`skip_to()` can often be implemented much more efficiently.

The final method of this group is :xapian-just-method:`check()`.  In some
cases, it's fairly cheap to check if a given document matches, but the
requirement that :xapian-just-method:`skip_to()` must leave the iteration
position on the next document is rather costly to implement (for example, it
might require linear scanning of document ids).  To avoid this where possible,
the :xapian-just-method:`check()` method allows the matcher to just check if a
given document matches.

The return value is :xapian-literal:`true` if the method leaves the iteration
position valid, and :xapian-literal:`false` if it doesn't.  In the latter case,
:xapian-just-method:`next()` will advance to the first matching position after
document id :xapian-variable:`did`, and :xapian-just-method:`skip_to()` will
act as it would if the iteration position was the first matching position after
:xapian-variable:`did`.

The default implementation of :xapian-just-method:`check()` is just a thin
wrapper around :xapian-just-method:`skip_to()` which returns
:xapian-literal:`true` - you should use this if :xapian-just-method:`skip_to()`
incurs only a small extra cost.  For our example, we match all documents so
there's no advantage to implementing :xapian-just-method:`check()`.

There's also a method :xapian-just-method:`get_description()` which returns
a string describing this object.  The default implementation returns a generic
answer.  This default is provided to avoid forcing you to provide an
implementation if you don't really care what
:xapian-just-method:`get_description()` gives for your sub-class.

.. todo:: Provide some more examples!
.. todo:: "why you might want to do this" (e.g. scenario) too

Multiple databases, and remote databases
========================================

In order to work with searches across multiple databases, or in remote
databases, some additional methods need to be implemented in your
:xapian-class:`PostingSource` subclass.  The first of these is
:xapian-just-method:`clone()`, which is used for multi database searches.  This
method should just return a newly allocated instance of the same posting source
class, initialised in the same way as the source that
:xapian-just-method:`clone()` was called on.  The returned source will be
deallocated by the caller (using "delete" - so you should allocate it with
"new").

If you don't care about supporting searches across multiple databases, you can
simply return NULL from this method.  In fact, the default implementation does
this, so you can just leave the default implementation in place.  If
:xapian-just-method:`clone()` returns NULL, an attempt to perform a search with
multiple databases will raise an exception:

.. code-block:: c++

    virtual PostingSource * clone() const;

Currently using custom :xapian-class:`PostingSource` subclasses with the remote
backend is only possible if the subclasses are implemented directly in C++.
To get this to work, you need to implement a few more methods.  Firstly, you
need to implement the :xapian-just-method:`name()` method.  This simply returns
the name of your posting source (fully qualified with any namespace):

.. code-block:: c++

    virtual std::string name() const;

Next, you need to implement the serialise and unserialise methods.  The
:xapian-just-method:`serialise()` method converts all the settings of the
PostingSource to a string, and the :xapian-just-method:`unserialise()` method
converts one of these strings back into a PostingSource.  Note that the
serialised string doesn't need to include any information about the current
iteration position of the PostingSource:

.. code-block:: c++

    virtual std::string serialise() const;
    virtual PostingSource * unserialise(const std::string &s) const;

Finally, you need to make a remote server which knows about your PostingSource.
Currently, the only way to do this is to modify the source slightly, and
compile your own xapian-tcpsrv.  To do this, you need to edit
``xapian-core/bin/xapian-tcpsrv.cc`` and find the
``register_user_weighting_schemes()`` function.  If ``MyPostingSource`` is your
posting source, at the end of this function, add these lines:

.. code-block:: c++

    Xapian::Registry registry;
    registry.register_postingsource(MyPostingSource());
    server.set_registry(registry);

.. todo:: Cover using a query-independent weight (e.g. from link analysis)
