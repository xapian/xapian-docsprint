.. Original content was taken from xapian-core/docs/deprecation.rst with
.. a copyright statement of:

.. This document was originally written by Richard Boulton.

.. Copyright (C) 2007 Lemur Consulting Ltd
.. Copyright (C) 2007-2026 Olly Betts

Features currently marked for deprecation
=========================================

.. note::

   We have a separate :ref:`list of all features that have been fully
   deprecated<deprecated-features>`, with the version they were removed.

Native C++ API
--------------

.. Keep table width to <= 126 columns.

========== ====== =================================== ========================================================================
Deprecated Remove Feature name                        Upgrade suggestion and comments
========== ====== =================================== ========================================================================
1.4.11     3.0.0  Environment variable                If you require Xapian >= 1.4.23, specify via the flags
                  ``XAPIAN_CJK_NGRAM``                ``Xapian::QueryParser::FLAG_NGRAMS``,
                                                      ``Xapian::TermGenerator::FLAG_NGRAMS`` and
                                                      ``Xapian::MSet::SNIPPET_NGRAMS`` instead.  If you want to be compatible
                                                      with Xapian < 1.4.23 too, use ``Xapian::QueryParser::FLAG_CJK_NGRAM``,
                                                      ``Xapian::TermGenerator::FLAG_CJK_NGRAM`` and
                                                      ``Xapian::MSet::SNIPPET_CJK_NGRAM``.
---------- ------ ----------------------------------- ------------------------------------------------------------------------
2.0.0      3.0.0  ``TradWeight`` class                Since 2.0.0, ``TradWeight`` is just a thin subclass of ``BM25Weight``.
                                                      Instead of ``TradWeight(k)`` use ``Xapian::BM25Weight(k, 0, 0, 1, 0)``;
                                                      instead of ``TradWeight()`` use ``Xapian::BM25Weight(1, 0, 0, 1, 0)``.
                                                      Both replacements work with all older Xapian versions too.
---------- ------ ----------------------------------- ------------------------------------------------------------------------
2.0.0      3.0.0  ``Enquire::set_expansion_scheme()`` Use ``"prob"`` instead, supported by Xapian >= 1.4.26.
                  with ``"trad""`` for eweightname
========== ====== =================================== ========================================================================

Bindings
--------

.. Keep table width to <= 126 columns.

========== ====== ======== ============================ ======================================================================
Deprecated Remove Language Feature name                 Upgrade suggestion and comments
========== ====== ======== ============================ ======================================================================
========== ====== ======== ============================ ======================================================================

Omega
-----

.. Keep table width to <= 126 columns.

========== ====== =================================== ========================================================================
Deprecated Remove Feature name                        Upgrade suggestion and comments
========== ====== =================================== ========================================================================
2.0.0      3.0.0  ``$set{weighting,trad k}`` and      Use ``$set{weighting,bm25 k 0 0 1 0}`` and
                  ``$set{weighting,trad}``            ``$set{weighting,bm25 1 0 0 1 0}`` instead.
========== ====== =================================== ========================================================================

.. Features currently marked as experimental
.. =========================================
.. Native C++ API
.. --------------
.. ============== ===============================================================================================================
.. Name           Details
.. ============== ===============================================================================================================
.. -------------- ---------------------------------------------------------------------------------------------------------------
.. ============== ===============================================================================================================
