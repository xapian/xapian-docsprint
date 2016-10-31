# Xapian documentation sprint

We're writing new introductory documentation for Xapian.  See the formatted
output at https://getting-started-with-xapian.readthedocs.org/

Join in on channel #xapian on irc.freenode.net (webchat link:
https://webchat.freenode.net/?channels=%23xapian).

This repository will be merged into the main Xapian tree and disappear
once ready.

You will need the Sphinx documentation tool installed to process the
documentation.  Confusingly there are several open source projects called
"Sphinx" - see http://sphinx-doc.org/install.html for tips on installing
the one you want (installing the `python-sphinx` package should work on
at least Debian, Fedora and Ubuntu).  We're unsure of the exact minimum version
requirement, but it's at least Sphinx 1.0.0 (the oldest we've tested with at
all recently was Sphinx 1.1.3).  Either the Python 2 or Python 3 version should
work.

You can generate versions for different programming languages (with translated
examples and adjustments to the text).  For full details see `make help`
but for example to generate an HTML version for C++ use:

```
make html LANGUAGE=c++
```
