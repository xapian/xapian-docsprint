.. _custom-weighting:

========================
Custom Weighting Schemes
========================

You can also implement your own weighting scheme, provided it can be expressed
in the form of a sum over the matching terms, plus an extra term which depends
on term-independent statistics (such as the normalised document length).

Currently it is only possible to implement custom weighting schemes in C++.
The API could probably be wrapped with a bit of effort, but performance is
likely to be disappointing as the :xapian-just-method:`get_sumpart()` method
gets called a lot (approximately once per matching term in each considered
document), so the overhead of routing a virtual method call from C++ to the
wrapped language will matter.

For example, here's an implementation of "coordinate matching" - each matching
term scores one point (this is provided in the API as
:xapian-class:`Xapian::CoordWeight` but is an illustrative example of
implementing a simple weighting scheme):

.. code-block:: c++

    class CoordWeight : public Xapian::Weight {
        double factor = 1.0;

      public:
        CoordWeight() { }

        ~CoordWeight() { }

        CoordWeight* clone() const override { return new CoordWeight; }

        void init(double factor_) override { factor = factor_; }

        std::string name() const override { return "coord"; }

        // No parameters to serialise.
        std::string serialise() const override { return std::string(); }

        CoordWeight* unserialise(const std::string&) const override {
            return new CoordWeight;
        }

        double get_sumpart(Xapian::termcount,
                           Xapian::termcount,
                           Xapian::termcount) const override {
            return factor;
        }
        double get_maxpart() const override { return factor; }

        double get_sumextra(Xapian::termcount,
                            Xapian::termcount) const override {
            return 0;
        }
        double get_maxextra() const override { return 0; }
    };


Implement a custom weighting scheme that requires various statistics
--------------------------------------------------------------------

The Coordinate scheme given above does not require any statistics. However,
custom weighting schemes that require various statistics such as average
document length in the database, the query length, total number of
documents in the collection etc. can also be implemented.

For that, the weighting scheme subclassed from :xapian-class:`Weight` simply needs
to "tell" :xapian-class:`Weight` which statistics it will be needing. This is done by
calling the :xapian-just-method:`need_stat(STATISTIC REQUIRED)` method in the
constructor of the subclassed weighting scheme. Note however, that only those
statistics which are absolutely required must be asked for as collecting
statistics is expensive.  For a full list of statistics currently available
from :xapian-class:`Weight` and the enumerators required to access them, please
refer to the `API documentation
<https://xapian.org/docs/apidoc/html/classXapian_1_1Weight.html#ae3c11f1d2d96a18e0eb9b9b31c5c5479>`_.

The statistics can then be obtained by the subclass by simply calling the
corresponding function of the :xapian-class:`Weight` class. For eg:- The document
frequency (Term frequency) of the term can be obtained by calling
:xapian-just-method:`get_termfreq()`. For a full list of functions required to
obtain various statistics, refer to
`the xapian/weight.h header file
<https://xapian.org/docs/sourcedoc/html/weight_8h_source.html#l00277>`_.

Example:- Consider a simple weighting scheme such as a pseudo Tf-Idf weighting
scheme which returns the document weight as the product of the within document
frequency of the term and the inverse of the term frequency
of the term (one divided by the number of documents the term appears in).

The implementation will be as follows:

.. code-block:: c++

    class PseudoTfIdfWeight : public Xapian::Weight {
        double factor = 1.0;

      public:
        PseudoTfIdfWeight() {
            need_stat(WDF);
            need_stat(TERMFREQ);
            need_stat(WDF_MAX);
        }

        ~PseudoTfIdfWeight() { }

        PseudoTfIdfWeight* clone() const override {
            return new PseudoTfIdfWeight;
        }

        void init(double factor_) override { factor = factor_; }

        std::string name() const override { return "pseudotfidf"; }

        // No parameters to serialise.
        std::string serialise() const override { return std::string(); }

        PseudoTfIdfWeight* unserialise(const std::string&) const override {
            return new PseudoTfIdfWeight;
        }

        double get_sumpart(Xapian::termcount wdf,
                           Xapian::termcount,
                           Xapian::termcount) const override {
            Xapian::doccount df = get_termfreq();
            double wdf_double(wdf);
            double wt = wdf_double / df;
            return wt * factor;
        }

        double get_maxpart() const override {
            Xapian::doccount df = get_termfreq();
            double max_wdf(get_wdf_upper_bound());
            double max_weight = max_wdf / df;
            return max_weight * factor;
        }

        double get_sumextra(Xapian::termcount,
                            Xapian::termcount) const override { return 0; }

        double get_maxextra() const override { return 0; }
    };


Note: The :xapian-just-method:`get_maxpart()` method returns an upper bound on
the weight returned by :xapian-just-method:`get_sumpart()`. In order to do
that, it requires the :xapian-just-constant:`WDF_MAX` statistic (the maximum
wdf of the term among all documents).
