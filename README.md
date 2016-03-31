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
the one you want.  We aren't certain exactly what version is needed - it
seems Sphinx 0.6.4 is too old but 1.1.3 is new enough.

For building a pdf version of documentation,you will need to install rst2pdf

Recommended method:

You can install rst2pdf from Python Package Index(PyPI) using pip
```sudo pip install rst2pdf```

Other Method:
If you want to build install rst2pdf from source

https://github.com/rst2pdf/rst2pdf#install-from-github

to generate a pdf version for C++ use:
```
make pdf SPHINXOPTS=-tc++
```
You can generate versions for different programming languages (with translated
examples and adjustments to the text).  For full details see `make help`
but for example to generate an HTML version for C++ use:

```
make html SPHINXOPTS=-tc++
```
