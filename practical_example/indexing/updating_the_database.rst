Updating the database
---------------------

If you look back at the verifying step of the database, you may notice
that the first item we have indexed has the word 'compass' spelled
incorrectly, which means that we will need to either update just that
document, or to re-index the entire database.

Reindexing the database can be done immediately using the :xapian-basename-code-example:`index1` script
we used for the initial indexing; this is because we are using an external
ID for each document we add to the database, taken from the `id_NUMBER`
field from the original data set. We then pass this to the :xapian-method:`Database::replace_document()`
method, which updates if there's already a document under that external ID,
or adds a document to the database otherwise.

In fact, because of this, :xapian-basename-code-example:`index1` can update just part of the
database. Just give it a file with only the rows that correspond to
documents that need updating. Everything else in the database will be
left untouched.

Deleting documents
~~~~~~~~~~~~~~~~~~

It is also possible to delete documents from the index using the
:xapian-method:`Database::delete_document()` method on a
:xapian-class:`WritableDatabase` object. This can be done either by Xapian docid
or using unique ID terms, as with :xapian-method:`Database::replace_document()`.

.. xapianexample:: delete1

A copy of this code is available in :xapian-code-example:`^`.

Then we just run our deletion tool, giving it identifiers taken from
the `id_NUMBER` field in the data set:

.. xapianrunexample:: index1
    :silent:
    :args: data/100-objects-v1.csv db

.. xapianrunexample:: delete1
    :args: db 1953-448 1985-438

After that, we expect to see two fewer documents in our database using xapian-delve:

.. code-block:: none

    $ xapian-delve db
    UUID = 1820ef0a-055b-4946-ae73-67aa4ef5c226
    number of documents = 98
    average document length = 100.041
    document length lower bound = 33
    document length upper bound = 251
    highest document id ever used = 100
    has positional information = true
