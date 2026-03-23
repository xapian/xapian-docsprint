.. Original content was taken from xapian-core/docs/sorting.rst with
.. a copyright statement of:
.. Copyright (C) 2007,2009,2011 Olly Betts

======================================
How to change how documents are scored
======================================

.. contents:: Table of contents

The easiest way to change document scoring is to change, or tune,
the weighting scheme in use; Xapian provides a number of weighting schemes,
including :xapian-class:`BM25Weight`, :xapian-class:`BM25PlusWeight`,
:xapian-class:`PL2Weight`, :xapian-class:`PL2PlusWeight`,
:xapian-class:`TfIdfWeight` and :xapian-class:`BoolWeight` (the default is
:xapian-class:`BM25Weight`).

You can also :ref:`implement your own <custom-weighting>`.

Built-in weighting schemes
==========================

The weighting schemes included with Xapian come from several families of
weighting schemes.

Probabilistic weighting schemes
-------------------------------

These weighting schemes are derived from Bayes' Theorem of conditional
probability.

TradWeight
~~~~~~~~~~

:xapian-class:`TradWeight` implemented the original probabilistic weighting
formula, which is essentially a special case of BM25 (it's BM25 with
:math:`k_2=0`, :math:`k_3=0`, :math:`b=1`, and :math:`minnormlen=0`, except
that prior to Xapian 2.0.0 all the weights are scaled by a constant factor).

Since Xapian 2.0.0, :xapian-class:`TradWeight` is just a thin sub-class of
:xapian-class:`BM25Weight` which sets these other parameter values (in older
releases :xapian-class:`TradWeight` was a separate subclass of
:xapian-class:`Weight` - the only functional difference is the scaling of the
returned weights by the constant factor mentioned above).
:xapian-class:`TradWeight` is also deprecated as of Xapian 2.0.0 - just use
:xapian-class:`BM25Weight` with the parameters shown above (which also works
with all older Xapian releases too).

BM25Weight
~~~~~~~~~~

The BM25 weighting formula which Xapian uses by default has a number of
parameters.  We have picked some default parameter values which do a good job
in general.  The optimal values of these parameters depend on the data being
indexed and the type of queries being run, so you may be able to improve the
effectiveness of your search system by adjusting these values, but it's a
fiddly process to tune them so people tend not to bother.

.. todo:: Say something more useful about tuning the parameters!

BM25PlusWeight
~~~~~~~~~~~~~~

BM25 may not properly reward occurrences of a query term in very long documents
so such documents may be overly penalised.  The BM25+ weighting formula aims
to improve ranking in this situation.

In BM25 there is a strict upper bound on the normalised Term Frequency
(:math:`k_1+1`).  However, the lower bound has not been well addressed
and the formula allows it to be negative (though most implementations,
including Xapian's, adjusts the result to prevent it being negative).

BM25+ was originally proposed by Lv-Zhai in CIKM11 paper: `Lower-Bounding Term
Frequency Normalization`_. It was derived from BM25 by lower-bounding TF.
It uses all of the parameters of BM25 with an additional parameter, delta
(:math:`\delta`).  Experiments by Lv-Zhai have shown that BM25+ works very well
with :math:`\delta=1`.

.. _Lower-Bounding Term Frequency Normalization: http://sifaka.cs.uiuc.edu/czhai/pub/cikm11-bm25.pdf

Divergence from Randomness
--------------------------

The idea behind Divergence from Randomness is to weight based on how much
the observed term distribution diverges from that which a random process
would produce.  Different models of that randomness can be used, as can
different normalisations, leading to a family of different models.  Xapian
implements several of these based on which have proved successful in
evaluations.

PL2Weight
~~~~~~~~~

The PL2 weighting scheme is useful for tasks that require early precision.

It uses thePoisson approximation of the Binomial Probabilistic distribution (P)
along with Stirling's approximation for the factorial value, the Laplace method
to find the after-effect of sampling (L) and the second wdf normalization
proposed by Amati to normalize the wdf in the document to the length of the
document (H2).

Document weight is controlled by parameter c. The default value of 1 for c is
suitable for longer queries but it may need to be changed for shorter queries.

PL2PLusWeight
~~~~~~~~~~~~~

Proposed by Lv-Zhai, PL2+ is a modified lower-bounded version of PL2,
with an additional parameter delta in addition to the parameter c from the PL2
weighting function.

Parameter delta is the pseudo tf value to control the scale of the tf lower
bound. It can be tuned for e.g from 0.1 to 1.5 in increments of 0.1 or so.
Although, PL2+ works effectively across collections with a fixed default value
of 0.8.

InL2Weight
~~~~~~~~~~

InL2 uses the Inverse document frequency model (In), the
Laplace method to find the aftereffect of sampling (L) and the second wdf
normalization proposed by Amati to normalize the wdf in the document to the
length of the document (H2).

This weighting scheme is useful for tasks that require early precision.

IfB2Weight
~~~~~~~~~~

IfB2 uses the Inverse term frequency model (If), the Bernoulli method to find
the aftereffect of sampling (B) and the second wdf normalization proposed
by Amati to normalize the wdf in the document to the length of the document
(H2).

IneB2Weight
~~~~~~~~~~~

IneB2 uses the Inverse expected document frequency model (Ine), the Bernoulli
method to find the aftereffect of sampling (B) and the second wdf
normalization proposed by Amati to normalize the wdf in the document to the
length of the document (H2).

BB2Weight
~~~~~~~~~

BB2 uses the Bose-Einstein probabilistic distribution (B) along with
Stirling's power approximation, the Bernoulli method to find the
aftereffect of sampling (B) and the second wdf normalization proposed by
Amati to normalize the wdf in the document to the length of the document
(H2).

DLHWeight
~~~~~~~~~

DLH is a parameter free weighting scheme and it should be used with query
expansion to obtain better results. It uses the HyperGeometric Probabilistic
model and Laplace's normalization to calculate the risk gain.

DPHWeight
~~~~~~~~~

DPH is a parameter free weighting scheme and it should be used with query
expansion to obtain better results. It uses the HyperGeometric Probabilistic
model and Popper's normalization to calculate the risk gain.

Unigram Language Modelling
--------------------------

These weighting schemes are based on the idea of statistically modelling
human languages.  "Unigram" means that words are assumed to occur
independently.  These schemes were developed by Bruce Croft and others.

Since not all terms appear in all documents, the wdf of some terms is zero
in some documents and we need to employ smoothing to avoid numerical problems.

Xapian 2.x provides :ref:`four different smoothing types<unigramlmweight>`, 
each implemented as a separate class.  Each takes further parameters to control
the effects of smoothing; we have picked some default parameter values which
should generally do a good job in each case.

Xapian 1.4.x provided a single :xapian-class:`LMWeight` class, but it was
discovered that this was using incorrect formulae for all the smoothing schemes.
It wasn't feasible to fix in 1.4.x so once we discovered the problem we advised
users not to use this class.

LM2StageWeight
~~~~~~~~~~~~~~

This implements two-stage smoothing, as described in Zhai, C., & Lafferty, J.D.
(2004). *A study of smoothing methods for language models applied to
information retrieval*. ACM Trans. Inf. Syst., 22, 179-214.

It takes two parameters, :math:`\lambda` and :math:`\mu`.

LMAbsDiscountWeight
~~~~~~~~~~~~~~~~~~~

This implements Absolute Discount smoothing, as described in Zhai, C., &
Lafferty, J.D.  (2004). *A study of smoothing methods for language models
applied to information retrieval*. ACM Trans. Inf. Syst., 22, 179-214.

It takes one parameter, :math:`\delta`.

LMDirichletWeight
~~~~~~~~~~~~~~~~~

This implements Dirichlet smoothing, and also the Dir+ variant.  The Dirichlet
prior method is one of the best performing language modeling approaches.  The
modified Dir+ version improves on the original as it is particularly more
effective across web collections including very long documents (where document
length is much larger than average document length).

Dirichlet smoothing is as described in Zhai, C., & Lafferty, J.D. (2004). *A
study of smoothing methods for language models applied to information
retrieval*. ACM Trans. Inf. Syst., 22, 179-214.

Dir+ is described in Lv, Y., & Zhai, C. (2011). *Lower-bounding term frequency
normalization*.  International Conference on Information and Knowledge
Management.

It takes two parameters, :math:`\mu` and :math:`\delta`.  If :math:`\delta=0`
then you get Dirichlet smoothing, while :math:`\delta>0` gives Dir+.

LMJMWeight
~~~~~~~~~~

This implements Jelinek-Mercer smoothing, as described in Zhai, C., & Lafferty,
J.D. (2004). *A study of smoothing methods for language models applied to
information retrieval*. ACM Trans. Inf. Syst., 22, 179-214.

It takes one parameter, :math:`\lambda`.

Tf-Idf models
-------------

.. FIXME blah blah blah!

TfIdfWeight
~~~~~~~~~~~

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

Apart from the three character string, these normalizations can also be specified by using three separate normalization parameters.

| 1. The first parameter specifies the normalization for the term frequency component (wdf_norm),
| 2. the second the normalization for the inverse document frequency component (idf_norm), and
| 3. the third the normalization used for the document weight (wt_norm).

1. | NONE
   | BOOLEAN
   | SQUARE
   | LOG
   | PIVOTED
   | LOG_AVERAGE
   | AUG_LOG
   | SQRT
   | AUG_AVERAGE

2. | TFIDF
   | NONE
   | PROB
   | FREQ
   | SQUARE
   | PIVOTED
   | GLOBAL_FREQ
   | LOG_GLOBAL_FREQ
   | INCREMENTED_GLOBAL_FREQ
   | SQRT_GLOBAL_FREQ

3. | NONE

Xapian 2.0.0 added support for the Piv+ normalisation to TfIdfWeight, which
represents one of the best performing vector space models. Piv+ takes two
parameters; slope and delta which are set to their default optimal values. You
may want pass different candidate values ranging from 0.1 to 1.5 and choose one
which fits best to your system based upon corpus being used.

.. _SMART normalization variants: https://nlp.stanford.edu/IR-book/html/htmledition/document-and-query-weighting-schemes-1.html

Other weighting schemes
-----------------------

These weighting schemes don't fall into a particular family.

BoolWeight
~~~~~~~~~~

BoolWeight assigns a weight of 0 to all documents, so the ordering is
determined solely by other factors.

CoordWeight
~~~~~~~~~~~

CoordWeight implements Coordinate Matching.  Each matching term scores one
point (e.g. see Managing Gigabytes, Second Edition p181).

It can be useful in some situations - for example, if you are implementing
a tag-based search and want to rank results by the number of matching tags.

DiceWeight
~~~~~~~~~~

DiceWeight ranks documents by the `Dice coefficient
<https://en.wikipedia.org/wiki/Dice-S%C3%B8rensen_coefficient>`_
measured between the query and each document.

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
