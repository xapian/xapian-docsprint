.. Copyright (C) 2007,2009,2011 Olly Betts

How to change how documents are scored
======================================

The document weighting schemes which Xapian includes by default are
``BM25Weight``, ``TradWeight`` and ``BoolWeight``.  The default is
BM25Weight.

BoolWeight
----------

BoolWeight assigns a weight of 0 to all documents, so the ordering is
determined solely by other factors.

TradWeight
----------

TradWeight implements the original probabilistic weighting formula, which
is essentially a special case of BM25 (it's BM25 with k2 = 0, k3 = 0, b =
1, and min_normlen = 0, except that all the weights are scaled by a
constant factor).

BM25Weight
----------

The BM25 weighting formula which Xapian uses by default has a number of
parameters.  We have picked some default parameter values which do a good job
in general.  The optimal values of these parameters depend on the data being
indexed and the type of queries being run, so you may be able to improve the
effectiveness of your search system by adjusting these values, but it's a
fiddly process to tune them so people tend not to bother.

.. todo:: Say something more useful about tuning the parameters!

See the `BM25 documentation <bm25.html>`_ for more details of BM25.

Custom Weighting Schemes
------------------------

You can also implement your own weighting scheme, provided it can be expressed
in the form of a sum over the matching terms, plus an extra term which depends
on term-independent statistics (such as the normalised document length).

For example, here's an implementation of "coordinate matching" - each matching
term scores one point::

    class CoordinateWeight : public Xapian::Weight {
      public:
	CoordinateWeight * clone() const { return new CoordinateWeight; }
	CoordinateWeight() { }
	~CoordinateWeight() { }

	std::string name() const { return "Coord"; }
	std::string serialise() const { return ""; }
	CoordinateWeight * unserialise(const std::string &) const {
	    return new CoordinateWeight;
	}

	Xapian::weight get_sumpart(Xapian::termcount, Xapian::doclength) const {
            return 1;
        }
	Xapian::weight get_maxpart() const { return 1; }

	Xapian::weight get_sumextra(Xapian::doclength) const { return 0; }
	Xapian::weight get_maxextra() const { return 0; }

	bool get_sumpart_needs_doclength() const { return false; }
    };

.. todo:: add a more complex example now that user-defined weight classes
          can see the statistics.
