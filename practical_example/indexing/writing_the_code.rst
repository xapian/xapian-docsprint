Let's write some code
---------------------

Here's the significant part of some example code to implement this index plan.

.. xapianexample:: index1
    :start-after: Start of example code
    :end-before: End of example code

A full copy of this code is available in :xapian_example_filename:`^`.

You can run this code to index a sample data file (held in
``data/100-objects-v1.csv``) to a database at path ``db`` as follows::

    python code/python/index1.py data/100-objects-v1.csv db

