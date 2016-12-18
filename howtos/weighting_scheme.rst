.. Original content was taken from xapian-core/docs/sorting.rst with
.. a copyright statement of:
.. Copyright (C) 2007,2009,2011 Olly Betts

======================================
How to change how documents are scored
======================================

.. contents:: Table of contents

The easiest way to change document scoring is to change, or tune,
the weighting scheme in use; Xapian provides a number of weighting schemes,
including ``BM25Weight``, ``BM25PlusWeight``, ``PL2Weight``, ``PL2PlusWeight``,
``LMWeight``, ``TfIdfWeight``, ``TradWeight`` and ``BoolWeight``
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

BM25+ was originally proposed by Lv-Zhai in CIKM11 paper: `Lower-Bounding Term Frequency
Normalization`_. BM25+ was derived from BM25 by lower-bounding TF and using all of the
parameters of BM25 with an additional parameter -- delta(δ). Experiments by Lv-Zhai have
shown that BM25+ works very well with δ = 1.

.. _Lower-Bounding Term Frequency Normalization: http://sifaka.cs.uiuc.edu/czhai/pub/cikm11-bm25.pdf

PL2Weight
---------

PL2Weight implements the representative scheme of the Divergence from Randomness Framework
This weighting scheme is useful for tasks that require early precision. It uses the
Poisson approximation of the Binomial Probabilistic distribution (P),the Laplace method
to find the after-effect of sampling (L) and the second wdf normalization to normalize the
wdf in the document to the length of the document (H2).

Document weight is controlled by parameter c. The default value of 1 for c is suitable
for longer queries but it may need to be changed for shorter queries.

PL2PLusWeight
-------------

Proposed by Lv-Zhai, PL2PlusWeight is the modified lower-bounded PL2 retrieval function of
the Divergence from Randomness Framework with an additonal parameter delta in addition to the
parameter c from the PL2 weighting function.

Parmater delta is the pseudo tf value to control the scale of the tf lower bound. It can be tuned
for e.g from 0.1 to 1.5 in increments of 0.1 or so. Although, PL2+ works effectively across collections
with a fixed default value of 0.8.

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

The Dirichlet prior method is one of the best performing language modeling approaches. Xapian
now provides support for a modified Dirichlet prior method, namely Dir+ which is an improvement over
the original as it is particularly more effective across web collections with very long documents
(where document length is much larger than average document length).

TfIdfWeight
-----------

TfIdfWeight implements the support for a number of `SMART normalization variants`_ of the tf-idf
weighting scheme. These normalizations are specified by a three character string:

| 1. The first letter in each string specifies the normalization for the term frequency component (wdfn),
| 2. the second the normalization for the inverse document frequency component (idfn), and
| 3. the third the normalization used for the document weight (wtn).

Normalizations are specified by the first character of their name string:

1. | "**n** one" : wdfn = wdf
   | "**b** oolean" (or sometimes binary) : wdfn = 1 if term is present in document else 0.
   | "**s** quare" : wdfn = wdf * wdf
   | "**l** og" : wdfn = 1 + ln (wdf)
   | "**P** ivoted" : wdfn = (1+log(1+log(wdf)))*(1/(1-slope+(slope*doclen/avg_len)))+delta [not in 1.4.x]

2. | "**n** one" : idfn = 1
   | "**t** fidf" : idfn = log (N / Termfreq) where N is the number of
                    documents in collection and Termfreq is the number of documents
   | "**p** rob" : idfn = log ((N - Termfreq) / Termfreq)
   | "**f** req" : idfn = 1 / Termfreq
   | "**s** quared" : idfn = log (N / Termfreq) ^ 2
   | "**P** ivoted" : idfn = log ((N + 1) / Termfreq) [not in 1.4.x]

3. | "**n** one" : wtn = wdfn * idfn

More recently supported normalization in TfIdfWeight is the pivoted (piv+) retrieval function
which represents one of the best performing vector space models. Piv+ takes two parameters; slope and delta
which are set to their default optimal values. You may want pass different candidate values ranging from 0.1
to 1.5 and choose one which fits best to your system based upon corpus being used.  Piv+ isn't supported
by 1.4.x, it's only in git master (and will be in the next release series) - it's hard to backport because
the two new parameters need to be stored by the TfIdfWeight class.

.. _SMART normalization variants: http://nlp.stanford.edu/IR-book/html/htmledition/document-and-query-weighting-schemes-1.html

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
