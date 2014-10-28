.. Original content was taken from xapian-core/docs/deprecation.rst with
.. a copyright statement of:

.. This document was originally written by Richard Boulton.

.. Copyright (C) 2007 Lemur Consulting Ltd
.. Copyright (C) 2007,2008,2009,2010,2011,2012,2013 Olly Betts

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
1.1.0      ?      Xapian::WritableDatabase::flush()   Xapian::WritableDatabase::commit() should be used instead.
========== ====== =================================== ========================================================================

.. flush() is just a simple inlined alias, so perhaps not worth causing pain by
.. removing it in a hurry, though it would be nice to be able to reuse the
.. method name to actually implement a flush() which writes out data but
.. doesn't commit.

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
