.. Original content was taken from xapian-core/docs/deprecation.rst with
.. a copyright statement of:

.. This document was originally written by Richard Boulton.

.. Copyright (C) 2007 Lemur Consulting Ltd
.. Copyright (C) 2007-2026 Olly Betts

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

We aim to make such changes in a way that allows developers to work with a
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
support (such as GCC, clang and MSVC) to emit compile-time warnings if these
features are used.

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

Releases are given three-part version numbers (e.g. 1.4.29), the three parts
being termed "major" (1), "minor" (4), and "revision" (29).

Starting with 2.0.0, releases with the same major version are termed a "stable
release series".  (For releases with major version 1, those with the same major
*and* minor formed a release series, with even minors being stable release series
and odd minors being development release series; releases with major version
0 were all essentially development releases.)

Within a stable release series, we strive to maintain API and ABI forwards
compatibility.  This means that an application written and compiled against
version `X.Y.a` of Xapian should work, without any source changes or need to
recompile, with a later version `X.Z.b` (where either `Z == Y` and `b >= a`,
or `Z > Y`).

A release which increases the major version number will usually change the ABI
incompatibly (so that code will need to be recompiled against the newer release
series).  A major version increase may also make incompatible API changes,
though we will attempt to do this in a way which makes it reasonably easy to
update applications such that they can work with two consecutive major
versions (and to document how to do so).

Users should generally be able to expect working code which uses Xapian not to
stop working without warning, so we have the following deprecation policy:

Normally a feature will be supported after being deprecated for an entire
stable release series.  Where technically feasible, we'll try to warn if a
deprecated feature is used, starting from the first X.0.0 release after it
is deprecated.

For example, if a feature is deprecated in release 2.0.0, it will be supported
for the entire 2.x.y release series but give a deprecation warning, and it will
be removed in 3.0.0.

Deprecation can happen mid-release series too.  If a feature is deprecated in
release 2.0.1 or 2.1.0, it will be supported for the 2.x.y *and* 3.x.y stable
release series, but will only give a deprecation warning starting with 3.0.0.
It won't be removed until 4.0.0.

This policy is an attempt to codify the stated aim, but the aim is more
important than the policy itself.  For example if we discover a feature which
doesn't actually work, it might be reasonable to start issuing a deprecation
warning right away and make an incompatible API change at the next ABI bump.

Experimental features
---------------------

Sometimes new features may be marked as "experimental".  Such features are
liable to change without going through the normal deprecation procedure.  This
includes changing on-disk formats for data stored by the feature, and breaking
API compatibility within a release series for the feature (however we won't
break ABI compatibility).  Such features are included in releases to get wider
use and corresponding feedback about them.

Deprecation in the bindings
---------------------------

When the Xapian C++ API changes, the interface provided by the Xapian bindings
will usually change in step.  In addition, it is sometimes necessary to change the
way in which Xapian is wrapped by bindings - for example, to provide a better
convenience wrapper for iterators in Python.  We aim to provide similar
compatibility guarantees for the APIs provided by the bindings as we do for the
C++ API.

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
8.1.x release was in 2001), and in some cases Linux distros continue to
support software after upstream stops.

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
   supports warnings about deprecated features (such as GCC), and check for
   such warnings.  Pass the -Werror flag to GCC to ensure that you don't miss
   any of them.

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
