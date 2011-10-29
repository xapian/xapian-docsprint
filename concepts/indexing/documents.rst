Documents
=========

A document in Xapian is simply an item which is returned by a search. When
building a new search system, the first decision to take is usually to
decide what the documents in your system are going to be. For example, for
a search over a website, there might be one document for each page of the
site. However, you could instead choose to use one document for each
paragraph of each page, or to group pages together into subjects and have
one document for each subject.

Documents have three components: `data`, `terms` and `values`.  They are
identified in a database by a unique integer id.  We'll discuss terms and
data first - values are useful for some more advanced search types.

Document Data
-------------

The `document data` is an arbitrary binary blob of data associated with the
document.  Xapian does nothing with this data other than store it in the
database and return it when requested. It can be used to hold a reference
to an external piece of information about the document (such as the primary
key in an external database table containing the document information), or
could be used to store the full text of the document. Generally, the best
thing to do with the document data is to store any information you need in
order to display the resulting document to the user (or to whatever process
consumes the results of searches).  There is no standard serialisation
scheme for putting structured data into the document data: depending on
your application, you might want to implement a simple scheme using
newlines to separate values, use JSON or XML serialisation, or use some
other method of pickling data.
