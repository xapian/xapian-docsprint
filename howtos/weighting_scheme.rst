.. Original content was taken from xapian-core/docs/sorting.rst with
.. a copyright statement of:
.. Copyright (C) 2007,2009,2011 Olly Betts

======================================
How to change how documents are scored
======================================

.. contents:: Table of contents

The easiest way to change document scoring is to change, or tune,
the weighting scheme in use; Xapian provides a number of weighting schemes,
including ``BM25Weight``, ``LMWeight``, ``TradWeight`` and ``BoolWeight``
(the default is BM25Weight).

You can also :ref:`implement your own <custom-weighting>`.

Built-in weighting schemes
==========================

BM25Weight
----------

The BM25 weighting formula which Xapian uses by default has a number of
parameters.  We have picked some default parameter values which do a good job
in general.  The optimal values of these parameters depend on the data being
indexed and the type of queries being run, so you may be able to improve the
effectiveness of your search system by adjusting these values, but it's a
fiddly process to tune them so people tend not to bother.

.. todo:: Say something more useful about tuning the parameters!

BM25PlusWeight
--------------

The occurrences of a query term in very long documents may not be rewarded properly
by BM25, and thus those very long documents could be overly penalized. In such cases, 
the BM25+ weighting formula is a useful improvement over the existing BM25 weighting 
formula. In BM25, it is easy to note that there is a strict upper bound (k1 + 1) for
Term Frequency normalization. However, the other interesting direction, lower-bounding
TF, has not been well addressed. 

Bm25+ was originally proposed by Lv-Zhai in CIKM11 paper: `Lower-Bounding Term Frequency
Normalization`_. BM25+ was derived from BM25 by lower-bounding TF and using all of the
parameters of BM25 with an additional parameter -- delta(δ). Experiments by Lv-Zhai have
shown that BM25+ works very well with δ = 1.

.. _Lower-Bounding Term Frequency Normalization: http://sifaka.cs.uiuc.edu/czhai/pub/cikm11-bm25.pdf

LMWeight (Unigram language modelling)
-------------------------------------

An important aspect of language model-based weighting is that, since not all
terms appear in all documents (and hence the wdf of some terms is zero with
respect to a given document), we have to employ smoothing to avoid problems.

Xapian provides :ref:`four different smoothing types<unigramlmweight>`, which take further parameters
to control the effects of smoothing; we have picked some default parameter
values which do a good job, using two stage smoothing.

The UnigramLM weighting formula is based on an original approach by Bruce Croft.
It uses statistical language modelling; 'unigram' in this case means that
words are considered to occur independently.

TradWeight
----------

TradWeight implements the original probabilistic weighting formula, which
is essentially a special case of BM25 (it's BM25 with k2 = 0, k3 = 0, b =
1, and min_normlen = 0, except that all the weights are scaled by a
constant factor).

BoolWeight
----------

BoolWeight assigns a weight of 0 to all documents, so the ordering is
determined solely by other factors.

Other approaches
================

Using an RSet to modify weights
-------------------------------

.. todo::

   This needs writing; it's also somewhat esoteric, and perhaps should be an
   advanced document or at least down-played.

Using a ValueWeightPostingSource
--------------------------------

.. todo::

   Combine ValueWeightPostingSource with OP_AND_MAYBE to add a constant weight
   for a particular (set of) document(s). This could be considered an advanced
   topic, so just a brief mention here and a complete document in advanced
   could be the best approach.
