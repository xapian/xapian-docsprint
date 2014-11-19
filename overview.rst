.. _overview:

============
Introduction
============

Xapian is an open source search engine library, which allows developers to
add advanced indexing and search facilities to their own applications.

This document aims to be a guide to getting up and running with your first
database, explaining basic concepts and providing code examples of the
library's core functionality.

If you just want to follow our code examples, you can skip the chapter on "Core
Concepts" and go straight to :ref:`a-practical-example` - but you should
probably make sure you have Xapian installed first!

.. note::

   If you're looking for a way of getting a search system running without
   having to write any code, you may want to look at `Omega
   <http://xapian.org/docs/omega/>`_, Xapian's pre-packaged web search
   application. It's designed so that as your needs grow, you can extend or
   even replace it without having to change your database; the structure
   that Omega sets up will work when you start writing code directly
   against Xapian.

Installation
------------

There are two pieces of Xapian you need to follow this guide: the
library itself, and support for the language you're going to be
using.  This guide was originally written with examples in Python_,
and we're also working on full translations into PHP_ and C++.  Help with
translating the examples into other languages would be most welcome.

.. _Python: http://www.python.org/
.. _PHP: http://www.php.net/

This guide documents Xapian 1.2 (except where a different version is explicitly
mentioned) so you'll find it easier to follow if you use a version from the 1.2
release series.  So let's get that onto your system.

Installation on Debian or Ubuntu
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Recent versions of both Debian and Ubuntu have Xapian 1.2 packaged: if
you're using Debian 6.0 (squeeze) or later, or Ubuntu 11.10 (Oneiric
Ocelot) or later you can just do one of the following depending on whether you
want to work through the examples in Python or C++::

    $ sudo apt-get install python-xapian
    $ sudo apt-get install libxapian-dev

If you're using Ubuntu 11.04 (Natty Narwhal) or earlier, you'll need to
install from our PPA_.

.. _PPA: https://launchpad.net/~xapian-backports/+archive/xapian-1.2

Packages of the PHP bindings aren't available due to a licence
compatibility issue, but you can `build your own packages
<http://trac.xapian.org/wiki/FAQ/PHP%20Bindings%20Package>`_.

Installation on other systems
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Many operating systems have packages available to make Xapian easy to
install; information is available on `our download page`_. This covers
most popular Linux distributions, FreeBSD, Mac OS (Python and C++
only) and Windows using Microsoft Visual Studio.

.. _our download page: http://xapian.org/download

.. _compile from source:

If you're using a different operating system, you will need to compile
from source, which should work on any Unix-like operating system,
and Windows using any one of Cygwin, MSYS+mingw or MSVC. Source code
is again available from our download page, as are additional Makefiles
for building using MSVC on Windows.

Datasets and example code
-------------------------

If you want to run the code we use to demonstrate Xapian's features
(and we recommend you do), you'll need both the code itself and the
two datasets we use.

The example code is available in Python, PHP, and C++ so far, although
there's only a complete set of examples for Python at present.

.. As mentioned before, you can get the `examples in
.. Python`_, `in PHP`_ and `in C++`_, although only the Python versions
.. are complete for now.

.. .. _examples in Python: http://xapian.org/docs/examples/python.tgz
.. .. _in PHP: http://xapian.org/docs/examples/php.tgz
.. .. _in C++: http://xapian.org/docs/examples/c++.tgz

.. todo:: finalise datasets and code and link to them from here

For now, you'll want to grab the `documentation source from github`_ which
contains the example code in each language, and also the data files listed
in the next paragraph (both are in the "code" subdirectory).

.. _documentation source from github: https://github.com/jaylett/xapian-docsprint

The first dataset is the first 100 objects taken from `museum
catalogue data released by the Science Museum
<http://api.sciencemuseum.org.uk/documentation/collections/>`_, and
the second we have curated ourselves from information on Wikipedia
about the 50 `US States
<http://en.wikipedia.org/wiki/U.S._state>`_. Both are provided as
gzipped CSV files. The first dataset is released under the `Creative
Commons license Attribution-NonCommercial-ShareAlike
<http://creativecommons.org/licenses/by-nc-sa/3.0/>`_ license, and the
second under `Creative Commons Attribution-Share Alike 3.0
<http://creativecommons.org/licenses/by-sa/3.0/>`_.

.. * `museum catalogue dataset <http://xapian.org/data/muscat-data.csv.gz>`_
.. * `US states dataset <http://xapian.org/data/states-data.csv.gz>`_

.. todo:: link to here from every howto and everything that needs the data files and example code
