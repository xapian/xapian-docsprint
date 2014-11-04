Database Modified
-----------------

If you're updating the same database you search from (rather than
updating a separate database and then "flipping" between them, using a
stub database), you may run into :xapian-class:`DatabaseModifiedError`, an
exception that can be raised while reading from the database. What
this means is that the database has changed too much since you opened
it for Xapian to be able to continue supplying you with
information. The solution here is to re-open the database with its
:xapian-just-method:`reopen()` method.

