# Xapian documentation sprint

This is the source for [Xapian's user
guide](https://getting-started-with-xapian.readthedocs.org/).
Eventually this repository will be merged into the main Xapian tree.

Join in on channel #xapian on irc.freenode.net (webchat link:
https://webchat.freenode.net/?channels=%23xapian) or via [our
mailing lists](https://xapian.org/lists).

You will need the [Sphinx documentation tool](http://sphinx-doc.org/)
installed to process the documentation. You can install the `python-sphinx`
package on Debian, Fedora and Ubuntu, or `pip install -r requirements.txt`
to install the python package directly. We currently support up to Sphinx
1.8.5, because we have yet to migrate our custom domain to python3.

You can generate versions for different programming languages (with translated
examples and adjustments to the text).  For full details see `make help`
but for example to generate an HTML version for C++ use:

```
make html LANGUAGE=c++
```

The default (when you run just `make html`) is to build for python.
