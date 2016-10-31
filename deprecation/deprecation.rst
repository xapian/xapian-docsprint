.. Original content was taken from xapian-core/docs/deprecation.rst with
.. a copyright statement of:

.. This document was originally written by Richard Boulton.

.. Copyright (C) 2007 Lemur Consulting Ltd
.. Copyright (C) 2007,2008,2009,2010,2011,2012,2013 Olly Betts

===========
Deprecation
===========

.. contents:: Table of contents

Introduction
============

Xapian's API is fairly stable and has been polished piece by piece over time,
but it still occasionally needs to be changed.  This may be because a new
feature has been implemented and the interface needs to allow access to it, but
it may also be required in order to polish a rough edge which has been missed
in earlier versions of Xapian, or simply to reflect an internal change which
requires a modification to the external interface.

We aim to make such changes in a way that allows developers to work against a
stable API, while avoiding the need for the Xapian developers to maintain too
many old historical interface artefacts.  This document describes the process
we use to deprecate old pieces of the API, lists parts of the API which are
currently marked as deprecated, and also describes parts of the API which have
been deprecated for some time, and are now removed from the Xapian library.

It is possible for functions, methods, constants, types or even whole classes
to be deprecated, but to save words this document will often use the term
"features" to refer collectively to any of these types of interface items.


Deprecation Procedure
=====================

Deprecation markers
-------------------

At any particular point, some parts of the C++ API will be marked as
"deprecated".  Deprecated features are annotated in the API headers with macros
such as ``XAPIAN_DEPRECATED()``, which will cause compilers with appropriate
support (such as GCC 3.1 or later, and MSVC 7.0 or later) to emit compile-time
warnings if these features are used.

If a feature is marked with one of these markers, you should avoid using it in
new code, and should migrate your code to use a replacement when possible.  The
documentation comments for the feature, or the list at the end
of this file, will describe possible alternatives to the deprecated feature.

If you want to disable deprecation warnings temporarily, you can do so
by passing ``"-DXAPIAN_DEPRECATED(X)=X"`` to the compiler (the quotes are
needed to protect the brackets from the shell).  If your build system uses
make, you might do this like so:

.. code-block:: sh

    make 'CPPFLAGS="-DXAPIAN_DEPRECATED(X)=X"'

API and ABI compatibility
-------------------------

Releases are given three-part version numbers (e.g. 1.2.9), the three parts
being termed "major" (1), "minor" (2), and "revision" (9).  Releases with
the same major and minor version are termed a "release series".

For Xapian releases 1.0.0 and higher, an even minor version indicates a stable
release series, while an odd minor version indicates a development release
series.

Within a stable release series, we strive to maintain API and ABI forwards
compatibility.  This means that an application written and compiled against
version `X.Y.a` of Xapian should work, without any source changes or need to
recompile, with a later version `X.Y.b`, for all `b` >= `a`.
Stable releases which increase the minor or major version number will usually
change the ABI incompatibly (so that code will need to be recompiled against
the newer release series.  They may also make incompatible API changes,
though we will attempt to do this in a way which makes it reasonably easy to
migrate applications, and document how to do so in this document.

It is possible that a feature may be marked as deprecated within a minor
release series - that is from version `X.Y.c`
onwards, where `c` is not zero.  The API and ABI will not be changed by this
deprecation, since the feature will still be available in the API (though the
change may cause the compiler to emit new warnings when rebuilding code
which uses the now-deprecated feature).

Users should generally be able to expect working code which uses Xapian not to
stop working without reason.  We attempt to codify this in the following
policy, but we reserve the right not to slavishly follow this.  The spirit of
the rule should kept in mind - for example if we discovered a feature which
didn't actually work, making an incompatible API change at the next ABI bump
would be reasonable.

Normally a feature will be supported after being deprecated for an entire
stable release series.  For example, if a feature is deprecated in release
1.2.0, it will be supported for the entire 1.2.x release series, and removed in
development release 1.3.0.  If a feature is deprecated in release 1.2.1, it
will be supported for the 1.2.x *and* 1.4.x stable release series (and of
course the 1.3.x release series in between), and won't be removed until
1.5.0.

Experimental features
---------------------

During a development release series (such as the 1.1.x series), some features
may be marked as "experimental".  Such features are liable to change without
going through the normal deprecation procedure.  This includes changing on-disk
formats for data stored by the feature, and breaking API and ABI compatibility
between releases for the feature.  Such features are included in releases to
get wider use and corresponding feedback about them.

Deprecation in the bindings
---------------------------

When the Xapian API changes, the interface provided by the Xapian bindings will
usually change in step.  In addition, it is sometimes necessary to change the
way in which Xapian is wrapped by bindings - for example, to provide a better
convenience wrapper for iterators in Python.  Again, we aim to ensure that an
application written (and compiled, if the language being bound is a compiled
language) for version `X.Y.a` of Xapian should work without any changes or need
to recompile, with a later version `X.Y.b`, for all `a` <= `b`.

However, the bindings are a little less mature than the core C++ API, so we
don't intend to give the same guarantee that a feature present and not
deprecated in version `X.Y.a` will work in all versions `X+1.Y.b`.  In other
words, we may remove features which have been deprecated without waiting for
an entire release series to pass.

Any planned deprecations will be documented in the list of deprecations and
removed features at the end of this file.

Support for Other Software
==========================

Support for other software doesn't follow the same deprecation rules as
for API features.

Our guiding principle for supporting version of other software is that
we don't aim to actively support versions which are no longer supported
"upstream".

So Xapian 1.1.0 doesn't support PHP4 because the PHP team no longer did
when it was released.  By the API deprecation rules we should have announced
this when Xapian 1.0.0 was released, but we don't have control over when and
to what timescales other software providers discontinue support for older
versions.

Sometimes we can support such versions without extra effort (e.g. Tcl's
stubs mechanism means Tcl 8.1 probably still works, even though the last
8.1.x release was over a decade ago), and in some cases Linux distros
continue to support software after upstream stops.

But in most cases keeping support around is a maintenance overhead and
we'd rather spend our time on more useful things.

Note that there's no guarantee that we will support and continue to
support versions just because upstream still does.  For example, we ceased
providing backported packages for Ubuntu dapper with Xapian 1.1.0 - in this
case, it's because we felt that if you're conservative enough to run dapper,
you'd probably prefer to stick with 1.0.x until you upgrade to hardy (the next
Ubuntu LTS release).  But we may decide not to support versions for other
reasons too.

How to avoid using deprecated features
======================================

We recommend taking the following steps to avoid depending on deprecated
features when writing your applications:

 - If at all possible, test compile your project using a compiler which
   supports warnings about deprecated features (such as GCC 3.1 or later), and
   check for such warnings.  Use the -Werror flag to GCC to ensure that you
   don't miss any of them.

 - Check the NEWS file for each new release for details of any new features
   which are deprecated in the release.

 - Check the documentation comments, or the automatically extracted API
   documentation, for each feature you use in your application.  This
   documentation will indicate features which are deprecated, or planned for
   deprecation.

 - For applications which are not written in C++, there is currently no
   equivalent of the ``XAPIAN_DEPRECATED`` macro for the bindings, and thus
   there is no way for the bindings to give a warning if a deprecated feature
   is used.  This would be a nice addition for those languages in which there
   is a reasonable way to give such warnings.  Until such a feature is
   implemented, all application writers using the bindings can do is to check
   the list of deprecated features in each new release, or lookup the features
   they are using in the list at the end of this file.


