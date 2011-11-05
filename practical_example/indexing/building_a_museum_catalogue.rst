Building a museum catalogue
===========================

We're going to build a simple search system based on museum catalogue data 
released under a Creative Commons license (By-NC-SA) by the Science Museum 
in London, UK.

http://api.sciencemuseum.org.uk/documentation/collections/

Preparing to run the examples
-----------------------------

To make things easier, we've extracted just the first 100 objects for the
museum catalogue data set and provide them as a gzipped CSV file,
``100-objects-v1.csv``.  This file, and the source code for the examples, can
be downloaded from http://xapian.org/data/muscat-data.tgz.  The following
discussion assumes you've downloaded that, unpacked it, and changed directory
to the top level directory in it.

.. todo:: Actually put the data and code in a tarball at this location.
