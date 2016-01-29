Building a museum catalogue
===========================

We're going to build a simple search system based on museum catalogue
data released under the `Creative Commons
Attribution-NonCommercial-ShareAlike
<https://creativecommons.org/licenses/by-nc-sa/3.0/>`_ license by the
`Science Museum in London, UK <http://www.sciencemuseum.org.uk/>`_.

Preparing to run the examples
-----------------------------

You should download both the two sample datasets and example code as
described in the :ref:`overview <overview>`,
and also check that you've installed Xapian as detailed there.

.. The code is provided as a gzipped tar file, which you should unpack
.. into the directory you're going to use while working through this
.. guide. The datasets are gzipped CSV files, which should be
.. uncompressed into the same directory. You should then open an
.. interactive shell in that directory. For instance, if you're using
.. Python for the examples, run something like the following::
.. 
..     $ mkdir xapian-guide
..     $ cd xapian-guide
..     $ wget https://xapian.org/docs/examples/python.tgz
..     $ wget https://xapian.org/data/muscat-data.csv.gz
..     $ wget https://xapian.org/data/states-data.csv.gz
..     $ gzip -dc python.tgz | tar xvf - && rm python.tgz
..     $ gzip -d muscat-data.csv.gz
..     $ gzip -d states-data.csv.gz
.. 
.. This will leave you with two files, `muscat.csv` and `states.csv`, and
.. a directory `code` which itself contains a directory `python` which
.. contains all the example code.
