Updating the database
---------------------

If you look back at the verifying step of the database, you may notice
that the first item we have indexed has the word 'compass' spelled
incorrectly, which means that we will need to either update just that
document, or to re-index the entire database.

Reindexing the database can be done immediately using the `index1.py` script
we used for the initial indexing; this is because we are using an external
ID for each document we add to the database, taken from the `id_NUMBER` 
field from the original data set. We then pass this to the `replace_document`
method, which updates if there's already a document under that external ID,
or adds a document to the database otherwise.

In fact, because of this, `index1.py` can update just part of the
database. Just give it a file with only the rows that correspond to
documents that need updating. Everything else in the database will be
left untouched.

Deleting documents
~~~~~~~~~~~~~~~~~~
It is also possible to delete documents from the index; for more 
information, see the documentation at http://xapian.org/ for details.
