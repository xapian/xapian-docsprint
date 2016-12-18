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
   <https://xapian.org/docs/omega/>`_, Xapian's pre-packaged web search
   application. It's designed so that as your needs grow, you can extend or
   even replace it without having to change your database; the structure
   that Omega sets up will work when you start writing code directly
   against Xapian.

Installation
------------

There are two pieces of Xapian you need to follow this guide: the
library itself, and support for the language you're going to be
using.  This guide was originally written with examples in Python_,
and we've made a start on full translations into Java, PHP_ and C++.
Help with completing these translations and with translating the examples
into other languages would be most welcome.

.. _Python: https://www.python.org/
.. _PHP: https://php.net/

This guide documents Xapian 1.4 (except where a different version is explicitly
mentioned) so you'll find it easier to follow if you use a version from the 1.4
release series.  So let's get that onto your system.

Installation on Debian or Ubuntu
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Neither Debian nor Ubuntu yet have a stable release with Xapian 1.4 packages.
If you're using Debian unstable or testing, there are 1.4 packages there.
For Ubuntu you can install packages from our PPA_.

.. _PPA: https://launchpad.net/~xapian-backports/+archive/ubuntu/ppa

Once you have a suitable repo configured, then you can do
one of the following depending on whether you want to work through the examples
in Python or C++:

.. code-block:: none

    $ sudo apt-get install python-xapian
    $ sudo apt-get install libxapian-dev

Packages of the PHP bindings aren't available due to a licence
compatibility issue, but you can `build your own packages
<https://trac.xapian.org/wiki/FAQ/PHP%20Bindings%20Package>`_.

Installation on other systems
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Many operating systems have packages available to make Xapian easy to
install; information is available on `our download page`_. This covers
most popular Linux distributions, FreeBSD, Mac OS (Python and C++
only) and Windows using Microsoft Visual Studio.

.. _our download page: https://xapian.org/download

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

The example code is available in Python, PHP, C++ and Java so far, although
there's only a complete set of examples for Python at present.

.. As mentioned before, you can get the `examples in
.. Python`_, `in PHP`_, `in C++`_ and `in Java`, although only the Python versions
.. are complete for now.

.. .. _examples in Python: https://xapian.org/docs/examples/python.tgz
.. .. _in PHP: https://xapian.org/docs/examples/php.tgz
.. .. _in C++: https://xapian.org/docs/examples/c++.tgz
.. .. _in Java: https://xapian.org/docs/examples/java.tgz

.. todo:: finalise datasets and code and link to them from here

For now, you'll want to grab the `documentation source from github`_ which
contains the example code in each language, and also the data files listed
in the next paragraph (both are in the "code" subdirectory).

.. _documentation source from github: https://github.com/xapian/xapian-docsprint

The first dataset is the first 100 objects taken from museum
catalogue data released by the `Science Museum
<http://www.sciencemuseum.org.uk>`_.  We downloaded this data from their API
site, but this has since shut down.  The second dataset we have curated
ourselves from information on Wikipedia about the 50 `US States
<https://en.wikipedia.org/wiki/U.S._state>`_. Both are provided as
gzipped CSV files. The first dataset is released under the `Creative
Commons license Attribution-NonCommercial-ShareAlike
<https://creativecommons.org/licenses/by-nc-sa/3.0/>`_ license, and the
second under `Creative Commons Attribution-Share Alike 3.0
<https://creativecommons.org/licenses/by-sa/3.0/>`_.

These datasets are in the git repo which holds the source for this
documentation - you can also view them online on `github
<https://github.com/xapian/xapian-docsprint/tree/master/data>`_:

 * `100-objects-v1.csv <https://raw.githubusercontent.com/xapian/xapian-docsprint/master/data/100-objects-v1.csv>`_
 * `100-objects-v2.csv <https://raw.githubusercontent.com/xapian/xapian-docsprint/master/data/100-objects-v2.csv>`_
 * `states.csv <https://raw.githubusercontent.com/xapian/xapian-docsprint/master/data/states.csv>`_

.. todo:: link to here from every howto and everything that needs the data files and example code

Contributing
------------

The `source for this documentation
<https://github.com/xapian/xapian-docsprint>`_ is being kept on github; the
best way to contribute is to add issues, comments and pull requests there.
We're monitoring IRC during the sprint sessions (and in general) so you can
also contact us on channel #xapian on irc.freenode.net [`webchat link
<https://webchat.freenode.net/?channels=%23xapian>`_].

To be able to generate this documentation from a git checkout, you'll need
the `Sphinx documentation tool <http://sphinx-doc.org/>`_.  If you're using
Debian or Ubuntu or another Debian-derived distro, you can get this by
installing either the `python-sphinx` or `python3-sphinx` package.  Once
you have Sphinx installed, you can generate HTML output with ``make html``
(for a full list of available formats, see ``make``).
