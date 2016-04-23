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
the one you want.  We aren't certain exactly what version is needed - at
least Sphinx 1.0.0 is needed, but the oldest we've actually tested with
recently was Sphinx 1.1.3.

You can generate versions for different programming languages (with translated
examples and adjustments to the text).  For full details see `make help`
but for example to generate an HTML version for C++ use:

```
make html LANGUAGE=c++
```
