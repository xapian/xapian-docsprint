Query authorisation
===================

Say you are building a system that allows people to write private
diary entries, and only share them with specific people. You wouldn't
want search to expose those entries to everyone, so you need to build
understanding of your authorisation scheme into the search system.

.. todo:: list up front the various methods

.. todo:: mention that omindex now indexes Unix user and group permissions.

Filtering results
-----------------

.. todo:: Discuss filtering results coming back from a query, and the problems
          with just doing that.

Putting authorisation data into the search index
------------------------------------------------

.. todo:: Discuss implementing auth schemes by indexing
          appropriate data.

Hybrid schemes
--------------

.. todo:: Discuss hybrid schemes (implementing auth using
          indexed terms, and also filtering results).

Timeliness of index authorisation
---------------------------------

.. todo:: Discuss issues relating
          to updates (in particular, how fast does something need to be hidden
          if it is changed to being private).
