# Xapian documentation sprint

This is the source for [Xapian's user
guide](https://getting-started-with-xapian.readthedocs.org/).
Eventually this repository will be merged into the main Xapian tree.

You will need the [Sphinx documentation tool](https://sphinx-doc.org/)
installed to process this documentation. You can install the `python-sphinx`
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

You can chat to us on matrix, IRC or via our mailing lists.  Links to
all of these are [on our website](https://xapian.org/lists).
