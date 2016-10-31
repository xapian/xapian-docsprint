.. Original content was taken from xapian-core/docs/deprecation.rst with
.. a copyright statement of:

.. This document was originally written by Richard Boulton.

.. Copyright (C) 2007 Lemur Consulting Ltd
.. Copyright (C) 2007,2008,2009,2010,2011,2012,2013,2015,2016 Olly Betts

Features currently marked for deprecation
=========================================

.. note::

   We have a separate :ref:`list of all features that have been fully
   deprecated<deprecated-features>`, with the version they were removed.

Native C++ API
--------------

.. Substitution definitions for feature names which are two wide for the column:

.. |set_max_wildcard_expansion| replace:: ``Xapian::QueryParser::set_max_wildcard_expansion()``
.. |flush| replace:: ``Xapian::WritableDatabase::flush()``
.. |VRP| replace:: ``Xapian::ValueRangeProcessor``
.. |DateVRP| replace:: ``Xapian::DateValueRangeProcessor``
.. |NumberVRP| replace:: ``Xapian::NumberValueRangeProcessor``
.. |StringVRP| replace:: ``Xapian::StringValueRangeProcessor``
.. |add_valuerangeprocessor| replace:: ``Xapian::QueryParser::add_valuerangeprocessor()``

.. Keep table width to <= 126 columns.

========== ====== =================================== ========================================================================
Deprecated Remove Feature name                        Upgrade suggestion and comments
========== ====== =================================== ========================================================================
1.3.1      1.5.0  ``Xapian::ErrorHandler``            We feel the current ErrorHandler API doesn't work at the right level (it
                                                      only works in Enquire, whereas you should be able to handle errors at
                                                      the Database level too) and we can't find any evidence that people are
                                                      actually using it.  So we've made the API a no-op and marked it as
                                                      deprecated.  The hope is to replace it with something better thought
                                                      out, probably during the 1.4.x release series.  There's some further
                                                      thoughts at https://trac.xapian.org/ticket/3#comment:8
---------- ------ ----------------------------------- ------------------------------------------------------------------------
1.3.2      1.5.0  ``Xapian::Auto::open_stub()``       Use the constructor with ``Xapian::DB_BACKEND_STUB`` flag (new in 1.3.2)
                                                      instead.
---------- ------ ----------------------------------- ------------------------------------------------------------------------
1.3.2      1.5.0  ``Xapian::Chert::open()``           Use the constructor with ``Xapian::DB_BACKEND_CHERT`` flag (new in
                                                      1.3.2) instead.
---------- ------ ----------------------------------- ------------------------------------------------------------------------
1.3.3      1.5.0  |set_max_wildcard_expansion|        Use ``Xapian::QueryParser::set_max_expansion()`` instead.
---------- ------ ----------------------------------- ------------------------------------------------------------------------
1.3.4      1.5.0  ``Xapian::Compactor`` methods       Use the ``Xapian::Database::compact()`` method instead.  The
                  ``set_block_size()``,               ``Xapian::Compact`` is now just a subclassable functor class to allow
                  ``set_renumber()``,                 access to progress messages and control over merging of user metadata.
                  ``set_multipass()``,
                  ``set_compaction_level()``,
                  ``set_destdir()``, ``add_source()`
                  and ``compact()``.
---------- ------ ----------------------------------- ------------------------------------------------------------------------
1.3.5      1.5.0  ``Xapian::PostingSource`` public    Use the respective getter and setter methods instead, added in 1.3.5 and
                  variables                           1.2.23.
---------- ------ ----------------------------------- ------------------------------------------------------------------------
1.3.5      1.5.0  ``Xapian::InMemory::open()``        Use the constructor with ``Xapian::DB_BACKEND_INMEMORY`` flag (new in
                                                      1.3.5) instead.
---------- ------ ----------------------------------- ------------------------------------------------------------------------
1.3.6      1.5.0  |flush|                             Use ``Xapian::WritableDatabase::commit()`` instead (available since
                                                      1.1.0).
---------- ------ ----------------------------------- ------------------------------------------------------------------------
1.3.6      1.5.0  Subclassing |VRP|                   Subclass ``Xapian::RangeProcessor`` instead, and return a
                                                      ``Xapian::Query`` from ``operator()()``.
---------- ------ ----------------------------------- ------------------------------------------------------------------------
1.3.6      1.5.0  Subclassing |DateVRP|               Subclass ``Xapian::DateRangeProcessor`` instead, and return a
                                                      ``Xapian::Query`` from ``operator()()``.
---------- ------ ----------------------------------- ------------------------------------------------------------------------
1.3.6      1.5.0  Subclassing |NumberVRP|             Subclass ``Xapian::NumberRangeProcessor`` instead, and return a
                                                      ``Xapian::Query`` from ``operator()()``.
---------- ------ ----------------------------------- ------------------------------------------------------------------------
1.3.6      1.5.0  Subclassing |StringVRP|             Subclass ``Xapian::RangeProcessor`` instead (which includes equivalent
                                                      support for prefix/suffix checking), and return a ``Xapian::Query`` from
                                                      ``operator()()``.
---------- ------ ----------------------------------- ------------------------------------------------------------------------
1.3.6      1.5.0  |add_valuerangeprocessor|           Use ``Xapian::QueryParser::add_rangeprocessor()`` instead, with a
                                                      ``Xapian::RangeProcessor`` object instead of a |VRP| object.
========== ====== =================================== ========================================================================

Bindings
--------

.. Keep table width to <= 126 columns.

========== ====== ======== ============================ ======================================================================
Deprecated Remove Language Feature name                 Upgrade suggestion and comments
========== ====== ======== ============================ ======================================================================
1.2.5      1.5.0  Python   MSet.items                   Iterate the MSet object itself instead.
---------- ------ -------- ---------------------------- ----------------------------------------------------------------------
1.2.5      1.5.0  Python   ESet.items                   Iterate the ESet object itself instead.
========== ====== ======== ============================ ======================================================================

Omega
-----

.. Keep table width to <= 126 columns.

========== ====== =================================== ========================================================================
Deprecated Remove Feature name                        Upgrade suggestion and comments
========== ====== =================================== ========================================================================
1.2.4      1.5.0  omindex command line long option    Renamed to ``--no-delete``, which works in 1.2.4 and later.
                  ``--preserve-nonduplicates``.
---------- ------ ----------------------------------- ------------------------------------------------------------------------
1.2.5      1.5.0  $set{spelling,true}                 Use $set{flag_spelling_suggestion,true} instead.
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
