==================
C++ Specific Notes
==================

Exceptions
==========

Xapian reports errors by throwing exceptions.  For generic failures
you will see exceptions derived from ``std::exception`` (for example,
``std::bad_alloc`` for a failure to allocate memory), but exceptions related
to Xapian-specific issues will be derived from ``Xapian::Error``.

Uncaught exceptions will cause your program to terminate, so it's wise
to at least have a top-level exception handler which can catch any
exceptions and report what they were.  You can call the ``get_description()``
method on a ``Xapian::Error`` object to get a human-readable string including
all the information the object contains.

Because ``Xapian::Error`` is an abstract base class you need to catch
it by reference:

.. xapiancodesnippet:: c++

    try {
        do_something_with_xapian();
    } catch (const Xapian::Error& e) {
        cout << "Exception: " << e.get_description() << '\n';
    } catch (const std::exception& e) {
        cout << "Exception: " << e.what() << '\n';
    }

There are two direct abstract subclasses of ``Xapian::Error`` - all
concrete subclasses are actually a subclass of one of these:

-  `Xapian::LogicError <https://xapian.org/docs/apidoc/html/classXapian_1_1LogicError.html>`_
   - for error conditions due to programming errors, such as a misuse of
   the API.  These indicate bugs, either in Xapian or in the application
   code.
-  `Xapian::RuntimeError <https://xapian.org/docs/apidoc/html/classXapian_1_1RuntimeError.html>`_
   - for error conditions due to run-time problems, such as failure to
   open a database.

The concrete subclasses allow an exception handler to distinguish different
types of problem by their types, for example:

.. xapiancodesnippet:: c++

    try {
        do_something_with_xapian();
    } catch (const Xapian::DatabaseOpeningError& e) {
        cout << "Problem opening database: " << e.get_description() << '\n';
    } catch (const Xapian::DatabaseCorruptError& e) {
        cout << "Database is corrupt: " << e.get_description() << '\n';
    } catch (const Xapian::DatabaseError& e) {
        cout << "(Other) database-related error: " << e.get_description() << '\n';
    } catch (const Xapian::Error& e) {
        cout << "Exception: " << e.get_description() << '\n';
    } catch (const std::bad_alloc& e) {
        cout << "Failed to allocate memory: " << e.what() << '\n';
    } catch (const std::exception& e) {
        cout << "Exception: " << e.what() << '\n';
    }

Object Copying
==============

Xapian objects are generally cheap to copy - either they are very lightweight
or they are thin wrappers around reference-counted pointers (a class design
pattern sometimes known as PIMPL for "Pointer to IMPLementation").

Object Ownership
================

API objects keep a reference to other API objects which they rely on the API
user generally doesn't need to worry about object lifetimes.

The exception is user-subclassable functors, for which Xapian's PIMPL approach
doesn't work (because the hidden implementation is what would need to be
subclassed).

By default, user code which creates such functor objects needs to manage their
lifetimes.  This can be awkward and potentially error-prone in cases where a
pointer to a functor is set by one API call and stored and then later used by
Xapian.  To address this problem, Xapian offers optional-reference counting for
such functor objects.  If you call :xapian-just-method:`release()` on a functor
object and pass it to a Xapian method then Xapian takes over ownership of the
object and will release it once it no longer needs it.  This tracking uses
reference counting so if you pass it to two Xapian methods the functor won't
be released until it's not needed by either.

An example of setting a :xapian-class:`Xapian::RangeProcessor` on a
:xapian-class:`Xapian::QueryParser`:

.. xapiancodesnippet:: c++

    qp.add_rangeprocessor((new Xapian::NumberRangeProcessor(0, "$"))->release());

This works for both built-in subclasses and user subclasses.

The name :xapian-just-method:`release()` is because this relinquishes ownership
in a similar way to ``std::unique_ptr::release()``

STL Compatibility
=================

API classes work as C++ STL compatible containers and iterators.

.. todo:: write me
