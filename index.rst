Getting Started with Xapian |version|
=====================================

Contents:

.. toctree::
   :maxdepth: 2

   overview
   language_specific
   concepts/index
   practical_example/index
   howtos/index
   advanced/index
   deprecation/index
   glossary
   LICENSE

Contributing
------------

The `source for this documentation
<http://github.com/xapian/xapian-docsprint>`_ is being kept on github; the
best way to contribute is to add issues, comments and pull requests there.
We're monitoring IRC during the sprint sessions (and in general) so you can
also contact us on channel #xapian on irc.freenode.net [`webchat link
<http://webchat.freenode.net/?channels=%23xapian>`_].

To be able to generate this documentation from a git checkout, you'll need
the `Sphinx documentation tool <http://sphinx-doc.org/>`_.  If you're using
Debian or Ubuntu or another Debian-derived distro, you can get this by
installing either the `python-sphinx` or `python3-sphinx` package.  Once
you have Sphinx installed, you can generate HTML output with ``make html``
(for a full list of available formats, see ``make``).
