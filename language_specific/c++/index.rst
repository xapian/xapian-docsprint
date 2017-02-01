==================
C++ Specific Notes
==================

Exceptions
==========

Xapian reports errors by throwing exceptions.  For failures in things like
memory allocation, you will see exceptions derived from ``std::exception``,
but exceptions related to Xapian-specific issues will be derived from
``Xapian::Error``.

Uncaught exceptions will cause your program to terminate, so it's wise
to at least have a top-level exception handler which can catch any
exceptions and report what they were.  You can call the ``get_description()``
method on a ``Xapian::Error`` object to get a human readable string including
all the information the object contains.

Because ``Xapian::Error`` is an abstract base class you need to catch
it by reference::

    try {
        do_something_with_xapian();
    } catch (const Xapian::Error & e) {
        cout << "Exception: " << e.get_description() << endl;
    } catch (const std::exception & e) {
        cout << "Exception: " << e.what() << endl;
    }

.. todo:: Xapian::Error hierarchy

Object Copying
==============

Objects are either reference counted handles or relatively cheap to copy.

Object Ownership
================

Creator owns.

.. todo:: write me

STL Compatibility
=================

.. todo:: write me
