.. _unigramlmweight:

===========================================
Tuning the Unigram Language Model: LMWeight
===========================================

.. contents:: Table of Contents

Unigram language modelling weighing scheme ranks document based on ability
to generate query from document language model. Unigram language model is
intuitive for user as they can think of term possible in document and add them
to query which will increase performance of weighing scheme in this setting.

Clamping Negative value
-----------------------

Since unigram language model differs from xapian way of weighing scheme as xapian
only support sum of various individual parts. Unigram language model have accommodated
product of probabilities by summing log of individual parts. Due to introduction of log
in probabilities a clamping factor to clamp negative value of log to positive is also
introduced.

The default value for the clamping parameter is the document length upper bound,
but the API user can adjust this value using the param_log parameter of the LMWeight
constructor.

Smoothing
---------

Unigram Language model foundation is document language model but due to length of document
document language model are usually sparse and affect the weight calculation for the documents
hence smoothing with collection frequency and document length is done. Xapian Implements
following Smoothing techniques:-

Dirichlet Prior Smoothing:
^^^^^^^^^^^^^^^^^^^^^^^^^^

Smoothing based on document size, because longer document require less smoothing
as they more accurately estimate language model.
Dirichlet Prior Smoothing is better at Estimation Role.

DP Smoothing technique is better for title or smaller queries as it is better
in estimation role.

Optimal Smoothing parameter

**param_smoothing1** - Small,Long Query - 2000

Jelinek Mercer Smoothing:
^^^^^^^^^^^^^^^^^^^^^^^^^

Combine relative frequency of query term with relative frequency in collection.
Address small sample problem and explain unobserved words in document.
JM Smoothing is better at explaining common and noisy words in query.
JM smoothing outperforms other smoothing schemes in Query Modelling.

This smoothing work better in case of noisy and long query as it DP smoothing is better in
Query Modelling.

Optimal Smoothing parameter

**param_smoothing1**  - Parameter range (0-1)

Small Query - 0.1 {Conjunctive interpolation of Query Term}
Longer Query - 0.7 {Disjunctive interpolation of Query Term}

Absolute Discounting Smoothing:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Absolute Discounting Smoothing is larger for flatter distribution of words.
More Smoothing for documents with relatively large count of unique terms.

Optimal Smoothing parameter

**param_smoothing1**  - Parameter range (0-1){Small,Long query - 0.7}


Two Stage Smoothing(Default):
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Two Stage smoothing is combination of Dirichlet Prior Smoothing and Jelinek Mercer Smoothing.
Two Stage smoothing is application of Jelinek-Mercer followed by Dirichlet Prior smoothing.
Jelinek-Mercer will first model the query and followed by Dirichlet Prior will account for missing and unseen terms.

Optimal Smoothing parameter

**param_smoothing1**

Parameter range (0-1)
Small Query - 0.1 {Conjunctive interpolation of Query Term}
Longer Query - 0.7 {Disjunctive interpolation of Query Term}

**param_smoothing2**

Small,Long Query - 2000

Constructor Parameters
----------------------

User can select parameters to clamp negative value and select smoothing scheme using. Xapian manages a enum for selection of smoothing technique:Following values need to be assigned to select_smoothing parameter to select smoothing type:

*Jelinek Mercer Smoothing - JELINEK_MERCER_SMOOTHING*

*Dirichlet Prior Smoothing - DIRICHLET_SMOOTHING*

*Absolute Discounting Smoothing - ABSOLUTE_DISCOUNT_SMOOTHING*

*Two Stage Smoothing - TWO_STAGE_SMOOTHING*


Following are Constructor provided by UnigramLM Weighting class. User can select constructor based on there requirement and number of parameter they want to provide. Refer generated documentation for constructor.

Selecting Weighting scheme:
---------------------------

Add following line in your code to select Unigram Language Model Weighting scheme::

    enquire.set_weighting_scheme(Xapian::LMWeight(700.0,Xapian::Weight::JELINEK_MERCER_SMOOTHING,0.4,2000,0.9));
