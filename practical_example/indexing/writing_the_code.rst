Let's write some code
---------------------

Here's the significant part of some example code to implement this index plan.

.. xapianexample:: index1

A full copy of this code is available in :xapian-code-example:`^`.

You can run this code to index a sample data file (held in
:xapian-example:`data/100-objects-v1.csv`) to a database at path ``db`` as follows:

.. xapianrunexample:: index1
    :cleanfirst: db
    :args: data/100-objects-v1.csv db
