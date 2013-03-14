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


Implement a custom weighting scheme that requires various statistics
--------------------------------------------------------------------

The Coordinate scheme given above does not require any statistics. However,
custom weighting schemes that require various statistics such as average
document length in the database, the query length, total number of
documents in the collection etc. can also be implemented.

For that, the weighting scheme subclassed from Xapian::Weight simply needs 
to "tell" Xapian::Weight which statistics it will be needing. This is done by
calling the need_stat(STATISTIC REQUIRED) function in the constructor of the
subclassed weighting scheme. Note however, that only those statistics which are
absolutely required must be asked for as collecting statistics is expensive.
For a full list of statistics currently available from Xapian::Weight and the
enumerators required to access them, please refer to: 
http://xapian.org/docs/sourcedoc/html/classXapian_1_1Weight.html#e3c11f1d2d96a18e0eb9b9b31c5c5479

The statistics can then be obtained by the subclass by simply calling the
corresponding function of the Xapian::Weight class. For eg:- The document
frequency (Term frequency) of the term can be obtained by calling
get_termfreq(). For a full list of functions required to obtain various 
statistics, refer:
http://xapian.org/docs/sourcedoc/html/weight_8h_source.html#l00277

Example:- Consider a simple weighting scheme such as a pseudo Tf-Idf weighting 
scheme which returns the document weight as the product of the within document
frequency of the term and the inverse of the document frequency
of the term (Inverse of the number of documents the term appears in).

The implementation will be as follows::

    class TfIdfWeight : public Xapian::Weight {
      public:
	TfIdfWeight * clone() const { return new TfIdfWeight; }
	TfIdfWeight() {
	    need_stat(WDF);
	    need_stat(TERMFREQ);
	    need_stat(WDF_MAX);
	}
	~TfIdfWeight() { }

	std::string name() const { return "TfIdf"; }
	std::string serialise() const { return ""; }
	TfIdfWeight * unserialise(const std::string &) const {
            return new TfIdfWeight;
	}

	Xapian::weight get_sumpart(Xapian::termcount wdf, Xapian::doclength) const {
            Xapian::doccount df = get_termfreq();
            double wdf_double(wdf);
            Xapian::weight wt = wdf_double / df;
            return wt; 
	}    

	Xapian::weight get_maxpart() const {
	    Xapian::doccount df = get_termfreq();
	    double max_wdf(get_wdf_upper_bound());
	    Xapian::weight max_weight = max_wdf / df;
	    return max_weight;
        }
	Xapian::weight get_sumextra(Xapian::doclength) const { return 0; }
	Xapian::weight get_maxextra() const { return 0; }	
    };


Note: The get_maxpart() function returns an upper bound on the weight returned
by get_sumpart(). In order to do that, it requires the WDF_MAX
statistic (the maximum wdf of the term among all documents). 
