Xapian documentation sprint
===========================

This is the source for `Xapian's user
guide <https://getting-started-with-xapian.readthedocs.org/>`_.
Eventually this repository will be merged into the main Xapian tree.

You will need the `Sphinx documentation tool <https://sphinx-doc.org/>`_
installed to process this documentation. You can install the `python3-sphinx`
or `python-sphinx` package on Debian, Fedora and Ubuntu, or ``pip install -r
requirements.txt`` to install the python package directly.

You can generate versions for different programming languages (with translated
examples and adjustments to the text).  For full details see ``make help``
but for example to generate an HTML version for C++ use::

    make html LANGUAGE=c++

The default if `LANGUAGE` isn't specified (e.g. when you run just ``make
html``) is to build for `python3`.

You can chat to us on matrix, IRC or via our mailing lists.  Links to
all of these are `on our website <https://xapian.org/lists>`_.
