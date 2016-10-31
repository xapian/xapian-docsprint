.. Original content was taken from xapian-core/docs/deprecation.rst with
.. a copyright statement of:

.. This document was originally written by Richard Boulton.

.. Copyright (C) 2007 Lemur Consulting Ltd
.. Copyright (C) 2007,2008,2009,2010,2011,2012,2013 Olly Betts

.. _deprecated-features:

============================
Features removed from Xapian
============================

.. contents:: Table of contents

Native C++ API
==============

.. Keep table width to <= 126 columns.

======= =================================== ==================================================================================
Removed Feature name                        Upgrade suggestion and comments
======= =================================== ==================================================================================
1.0.0   QueryParser::set_stemming_options() Use ``set_stemmer()``, ``set_stemming_strategy()`` and/or ``set_stopper()``
                                            instead:

                                            - ``set_stemming_options("")`` becomes
                                              ``set_stemming_strategy(Xapian::QueryParser::STEM_NONE)``

                                            - ``set_stemming_options("none")`` becomes
                                              ``set_stemming_strategy(Xapian::QueryParser::STEM_NONE)``

                                            - ``set_stemming_options(LANG)`` becomes
                                              ``set_stemmer(Xapian::Stem(LANG)`` and
                                              ``set_stemming_strategy(Xapian::QueryParser::STEM_SOME)``

                                            - ``set_stemming_options(LANG, false)`` becomes
                                              ``set_stemmer(Xapian::Stem(LANG)`` and
                                              ``set_stemming_strategy(Xapian::QueryParser::STEM_SOME)``

                                            - ``set_stemming_options(LANG, true)`` becomes
                                              ``set_stemmer(Xapian::Stem(LANG)`` and
                                              ``set_stemming_strategy(Xapian::QueryParser::STEM_ALL)``

                                            If a third parameter is passed, ``set_stopper(PARAM3)`` and treat the first two
                                            parameters as above.
------- ----------------------------------- ----------------------------------------------------------------------------------
1.0.0   Enquire::set_sort_forward()         Use ``Enquire::set_docid_order()`` instead:

                                             - ``set_sort_forward(true)`` becomes ``set_docid_order(ASCENDING)``
                                             - ``set_sort_forward(false)`` becomes ``set_docid_order(DESCENDING)``
------- ----------------------------------- ----------------------------------------------------------------------------------
1.0.0   Enquire::set_sorting()              Use ``Enquire::set_sort_by_relevance()``, ``Enquire::set_sort_by_value()``, or
                                            ``Enquire::set_sort_by_value_then_relevance()`` instead.

                                             - ``set_sorting(KEY, 1)`` becomes ``set_sort_by_value(KEY)``
                                             - ``set_sorting(KEY, 1, false)`` becomes ``set_sort_by_value(KEY)``
                                             - ``set_sorting(KEY, 1, true)`` becomes ``set_sort_by_value_then_relevance(KEY)``
                                             - ``set_sorting(ANYTHING, 0)`` becomes ``set_sort_by_relevance()``
                                             - ``set_sorting(Xapian::BAD_VALUENO, ANYTHING)`` becomes
                                               ``set_sort_by_relevance()``
------- ----------------------------------- ----------------------------------------------------------------------------------
1.0.0   Stem::stem_word(word)               Use ``Stem::operator()(word)`` instead.
------- ----------------------------------- ----------------------------------------------------------------------------------
1.0.0   Auto::open(path)                    Use the ``Database(path)`` constructor instead.
------- ----------------------------------- ----------------------------------------------------------------------------------
1.0.0   Auto::open(path, action)            Use the ``WritableDatabase(path, action)`` constructor instead.
------- ----------------------------------- ----------------------------------------------------------------------------------
1.0.0   Query::is_empty()                   Use ``Query::empty()`` instead.
------- ----------------------------------- ----------------------------------------------------------------------------------
1.0.0   Document::add_term_nopos()          Use ``Document::add_term()`` instead.
------- ----------------------------------- ----------------------------------------------------------------------------------
1.0.0   Enquire::set_bias()                 Use ``PostingSource`` instead (new in 1.2).
------- ----------------------------------- ----------------------------------------------------------------------------------
1.0.0   ExpandDecider::operator()           Return type is now ``bool`` not ``int``.
------- ----------------------------------- ----------------------------------------------------------------------------------
1.0.0   MatchDecider::operator()            Return type is now ``bool`` not ``int``.
------- ----------------------------------- ----------------------------------------------------------------------------------
1.0.0   Error::get_type()                   Return type is now ``const char *`` not ``std::string``.  Most existing code
                                            won't need changes, but if it does the simplest fix is to write
                                            ``std::string(e.get_type())`` instead of ``e.get_type()``.
------- ----------------------------------- ----------------------------------------------------------------------------------
1.0.0   <xapian/output.h>                   Use ``cout << obj.get_description();`` instead of ``cout << obj;``
------- ----------------------------------- ----------------------------------------------------------------------------------
1.0.0   Several constructors marked         Explicitly create the object type required, for example use
        as explicit.                        ``Xapian::Enquire enq(Xapian::Database(path));`` instead of
                                            ``Xapian::Enquire enq(path);``
------- ----------------------------------- ----------------------------------------------------------------------------------
1.0.0   QueryParser::parse_query() throwing Catch ``Xapian::QueryParserError`` instead of ``const char *``, and call
        ``const char *`` exception.         ``get_msg()`` on the caught object.  If you need to build with either version,
                                            catch both (you'll need to compile the part which catches ``QueryParserError``
                                            conditionally, since this exception isn't present in the 0.9 release series).
------- ----------------------------------- ----------------------------------------------------------------------------------
1.1.0   xapian_version_string()             Use ``version_string()`` instead.
------- ----------------------------------- ----------------------------------------------------------------------------------
1.1.0   xapian_major_version()              Use ``major_version()`` instead.
------- ----------------------------------- ----------------------------------------------------------------------------------
1.1.0   xapian_minor_version()              Use ``minor_version()`` instead.
------- ----------------------------------- ----------------------------------------------------------------------------------
1.1.0   xapian_revision()                   Use ``revision()`` instead.
------- ----------------------------------- ----------------------------------------------------------------------------------
1.1.0   Enquire::include_query_terms        Use ``Enquire::INCLUDE_QUERY_TERMS`` instead.
------- ----------------------------------- ----------------------------------------------------------------------------------
1.1.0   Enquire::use_exact_termfreq         Use ``Enquire::USE_EXACT_TERMFREQ`` instead.
------- ----------------------------------- ----------------------------------------------------------------------------------
1.1.0   Error::get_errno()                  Use ``Error::get_error_string()`` instead.
------- ----------------------------------- ----------------------------------------------------------------------------------
1.1.0   Enquire::register_match_decider()   This method didn't do anything, so just remove calls to it!
------- ----------------------------------- ----------------------------------------------------------------------------------
1.1.0   Query::Query(Query::op, Query)      This constructor isn't useful for any currently implemented
                                            ``Query::op``.
------- ----------------------------------- ----------------------------------------------------------------------------------
1.1.0   The Quartz backend                  Use the Chert backend instead.
------- ----------------------------------- ----------------------------------------------------------------------------------
1.1.0   Quartz::open()                      Use ``Chert::open()`` instead.
------- ----------------------------------- ----------------------------------------------------------------------------------
1.1.0   quartzcheck                         Use ``xapian-check`` instead.
------- ----------------------------------- ----------------------------------------------------------------------------------
1.1.0   quartzcompact                       Use ``xapian-compact`` instead.
------- ----------------------------------- ----------------------------------------------------------------------------------
1.1.0   quartzdump                          Use ``xapian-inspect`` instead.
------- ----------------------------------- ----------------------------------------------------------------------------------
1.1.0   configure --enable-debug            configure --enable-assertions
------- ----------------------------------- ----------------------------------------------------------------------------------
1.1.0   configure --enable-debug=full       configure --enable-assertions --enable-log
------- ----------------------------------- ----------------------------------------------------------------------------------
1.1.0   configure --enable-debug=partial    configure --enable-assertions=partial
------- ----------------------------------- ----------------------------------------------------------------------------------
1.1.0   configure --enable-debug=profile    configure --enable-log=profile
------- ----------------------------------- ----------------------------------------------------------------------------------
1.1.0   configure --enable-debug-verbose    configure --enable-log
------- ----------------------------------- ----------------------------------------------------------------------------------
1.1.0   ``Database::positionlist_begin()``  This check is quite expensive, and often you don't care.  If you
        throwing ``RangeError`` if the      do it's easy to check - just open a ``TermListIterator`` for the
        term specified doesn't index the    document and use ``skip_to()`` to check if the term is there.
        document specified.
------- ----------------------------------- ----------------------------------------------------------------------------------
1.1.0   ``Database::positionlist_begin()``  This check is quite expensive, and often you don't care.  If you
        throwing ``DocNotFoundError`` if    do, it's easy to check - just call ``Database::get_document()`` with the
        the document specified doesn't      specified document ID.
        exist.
------- ----------------------------------- ----------------------------------------------------------------------------------
1.1.5   delve -k                            Accepted as an undocumented alias for -V since 0.9.10 for compatibility with 0.9.9
                                            and earlier.  Just use -V instead.
------- ----------------------------------- ----------------------------------------------------------------------------------
1.3.0   The Flint backend                   Use the Chert backend instead.
------- ----------------------------------- ----------------------------------------------------------------------------------
1.3.0   Flint::open()                       Use ``Chert::open()`` instead.
------- ----------------------------------- ----------------------------------------------------------------------------------
1.3.0   xapian-chert-update                 Install Xapian 1.2.x (where x >= 5) to update chert databases from 1.1.3 and
                                            earlier.
------- ----------------------------------- ----------------------------------------------------------------------------------
1.3.0   Default second parameter to         The parameter name was ``ascending`` and defaulted to ``true``.  However
        ``Enquire`` sorting functions.      ascending=false gave what you'd expect the default sort order to be (and probably
                                            think of as ascending) while ascending=true gave the reverse (descending) order.
                                            For sanity, we renamed the parameter to ``reverse`` and deprecated the default
                                            value.  In the more distant future, we'll probably add a default again, but of
                                            ``false`` instead.

                                            The methods affected are:
                                            ``Enquire::set_sort_by_value(Xapian::valueno sort_key)``
                                            ``Enquire::set_sort_by_key(Xapian::Sorter * sorter)``
                                            ``Enquire::set_sort_by_value_then_relevance(Xapian::valueno sort_key)``
                                            ``Enquire::set_sort_by_key_then_relevance(Xapian::Sorter * sorter)``
                                            ``Enquire::set_sort_by_relevance_then_value(Xapian::valueno sort_key)``
                                            ``Enquire::set_sort_by_relevance_then_key(Xapian::Sorter * sorter)``

                                            To update them, just add a second parameter with value ``true`` to each of the
                                            above calls.  For the methods which take a ``Xapian::Sorter`` object, you'll also
                                            need to migrate to ``Xapian::KeyMaker`` (see below).
------- ----------------------------------- ----------------------------------------------------------------------------------
1.3.0   ``Sorter`` abstract base class.     Use ``KeyMaker`` class instead, which has the same semantics, but has been renamed
                                            to indicate that the keys produced may be used for purposes other than sorting (we
                                            plan to allow collapsing on generated keys in the future).
------- ----------------------------------- ----------------------------------------------------------------------------------
1.3.0   ``MultiValueSorter`` class.         Use ``MultiValueKeyMaker`` class instead.  Note that ``MultiValueSorter::add()``
                                            becomes ``MultiValueKeyMaker::add_value()``, but the sense of the direction flag
                                            is reversed (to be consistent with ``Enquire::set_sort_by_value()``), so::

                                                MultiValueSorter sorter;
                                                // Primary ordering is forwards on value 4.
                                                sorter.add(4);
                                                // Secondary ordering is reverse on value 5.
                                                sorter.add(5, false);

                                            becomes::

                                                MultiValueKeyMaker sorter;
                                                // Primary ordering is forwards on value 4.
                                                sorter.add_value(4);
                                                // Secondary ordering is reverse on value 5.
                                                sorter.add_value(5, true);
------- ----------------------------------- ----------------------------------------------------------------------------------
1.3.0   ``matchspy`` parameter to           Use the newer ``MatchSpy`` class and ``Enquire::add_matchspy()`` method instead.
        ``Enquire::get_mset()``
------- ----------------------------------- ----------------------------------------------------------------------------------
1.3.0   ``Xapian::timeout`` typedef         Use ``unsigned`` instead, which should also work with older Xapian releases.
------- ----------------------------------- ----------------------------------------------------------------------------------
1.3.0   ``Xapian::percent`` typedef         Use ``int`` instead, which should also work with older Xapian releases.
------- ----------------------------------- ----------------------------------------------------------------------------------
1.3.0   ``Xapian::weight`` typedef          Use ``double`` instead, which should also work with older Xapian releases.
------- ----------------------------------- ----------------------------------------------------------------------------------
1.3.0   ``Xapian::Query::unserialise()``    To be compatible with older and newer Xapian, you can catch both exceptions.
        throws
        ``Xapian::SerialisationError`` not
        ``Xapian::InvalidArgumentError``
        for errors in serialised data
------- ----------------------------------- ----------------------------------------------------------------------------------
1.3.2   The Brass backend                   Use the Glass backend instead.
------- ----------------------------------- ----------------------------------------------------------------------------------
1.3.2   ``Xapian::Brass::open()``           Use the constructor with ``Xapian::DB_BACKEND_GLASS`` flag (new in 1.3.2) instead.
------- ----------------------------------- ----------------------------------------------------------------------------------
1.3.4   Copy constructors and assignment    We think it was a mistake that implicit copy constructors and assignment operators
        operators for classes:              were being provided for these functor classes - it's hard to use them correctly,
        ``Xapian::ExpandDecider``,          but easy to use them in ways which compile but don't work correctly, and we doubt
        ``Xapian::FieldProcessor`` (new in  anyone is intentionally using them, so we've simply removed them.  For more
        1.3.1), ``Xapian::KeyMaker``,       information, see https://trac.xapian.org/ticket/681
        ``Xapian::MatchDecider``,
        ``Xapian::StemImplementation``,
        ``Xapian::Stopper`` and
        ``Xapian::ValueRangeProcessor``.
------- ----------------------------------- ----------------------------------------------------------------------------------
1.3.5   ``Xapian::DBCHECK_SHOW_BITMAP``     Use ``Xapian::DBCHECK_SHOW_FREELIST`` (added in 1.3.2) instead.
                                            ``Xapian::DBCHECK_SHOW_BITMAP`` was added in 1.3.0, so has never been in a stable
                                            release.
======= =================================== ==================================================================================


Bindings
========

.. Keep table width to <= 126 columns.

======= ======== ============================ ================================================================================
Removed Language Feature name                 Upgrade suggestion and comments
======= ======== ============================ ================================================================================
1.0.0   SWIG     Enquire::set_sort_forward()  Use ``Enquire::set_docid_order()`` instead.
        [#rswg]_
                                                - ``set_sort_forward(true)`` becomes ``set_docid_order(ASCENDING)``
                                                - ``set_sort_forward(false)`` becomes ``set_docid_order(DESCENDING)``
------- -------- ---------------------------- --------------------------------------------------------------------------------
1.0.0   SWIG     Enquire::set_sorting()       Use ``Enquire::set_sort_by_relevance()``, ``Enquire::set_sort_by_value()``
        [#rswg]_                              or ``Enquire::set_sort_by_value_then_relevance()`` instead.

                                               - ``set_sorting(KEY, 1)`` becomes ``set_sort_by_value(KEY)``
                                               - ``set_sorting(KEY, 1, false) becomes ``set_sort_by_value(KEY)``
                                               - ``set_sorting(KEY, 1, true)`` becomes
                                                 ``set_sort_by_value_then_relevance(KEY)``
                                               - ``set_sorting(ANYTHING, 0) becomes set_sort_by_relevance()``
                                               - ``set_sorting(Xapian::BAD_VALUENO, ANYTHING)`` becomes
                                                 ``set_sort_by_relevance()``
------- -------- ---------------------------- --------------------------------------------------------------------------------
1.0.0   SWIG     Auto::open(path)             Use the ``Database(path)`` constructor instead.
        [#rswg]_

------- -------- ---------------------------- --------------------------------------------------------------------------------
1.0.0   SWIG     Auto::open(path, action)     Use the ``WritableDatabase(path, action)`` constructor instead.
        [#rswg]_
------- -------- ---------------------------- --------------------------------------------------------------------------------
1.0.0   SWIG     MSet::is_empty()             Use ``MSet::empty()`` instead.
        [#rsw3]_
------- -------- ---------------------------- --------------------------------------------------------------------------------
1.0.0   SWIG     ESet::is_empty()             Use ``ESet::empty()`` instead.
        [#rsw3]_
------- -------- ---------------------------- --------------------------------------------------------------------------------
1.0.0   SWIG     RSet::is_empty()             Use ``RSet::empty()`` instead.
        [#rsw3]_
------- -------- ---------------------------- --------------------------------------------------------------------------------
1.0.0   SWIG     Query::is_empty()            Use ``Query::empty()`` instead.
        [#rsw3]_
------- -------- ---------------------------- --------------------------------------------------------------------------------
1.0.0   SWIG     Document::add_term_nopos()   Use ``Document::add_term()`` instead.
        [#rswg]_
------- -------- ---------------------------- --------------------------------------------------------------------------------
1.0.0   CSharp   ExpandDecider::Apply()       Return type is now ``bool`` instead of ``int``.
------- -------- ---------------------------- --------------------------------------------------------------------------------
1.0.0   CSharp   MatchDecider::Apply()        Return type is now ``bool`` instead of ``int``.
------- -------- ---------------------------- --------------------------------------------------------------------------------
1.0.0   SWIG     Stem::stem_word(word)        Use ``Stem::operator()(word)`` instead. [#callable]_
        [#rswg]_
------- -------- ---------------------------- --------------------------------------------------------------------------------
1.1.0   SWIG     xapian_version_string()      Use ``version_string()`` instead.
        [#rswg]_
------- -------- ---------------------------- --------------------------------------------------------------------------------
1.1.0   SWIG     xapian_major_version()       Use ``major_version()`` instead.
        [#rswg]_
------- -------- ---------------------------- --------------------------------------------------------------------------------
1.1.0   SWIG     xapian_minor_version()       Use ``minor_version()`` instead.
        [#rswg]_
------- -------- ---------------------------- --------------------------------------------------------------------------------
1.1.0   SWIG     xapian_revision()            Use ``revision()`` instead.
        [#rswg]_
------- -------- ---------------------------- --------------------------------------------------------------------------------
1.1.0   SWIG     ESetIterator::get_termname() Use ``ESetIterator::get_term()`` instead.  This change is intended to
        [#rswg]_                              bring the ESet iterators in line with other term iterators, which all
                                              support ``get_term()`` instead of ``get_termname()``.

------- -------- ---------------------------- --------------------------------------------------------------------------------
1.1.0   Python   get_description()            All ``get_description()`` methods have been renamed to ``__str__()``,
                                              so the normal python ``str()`` function can be used.
------- -------- ---------------------------- --------------------------------------------------------------------------------
1.1.0   Python   MSetItem.get_*()             All these methods are deprecated, in favour of properties.
                                              To convert, just change ``msetitem.get_FOO()`` to ``msetitem.FOO``
------- -------- ---------------------------- --------------------------------------------------------------------------------
1.1.0   Python   Enquire.get_matching_terms   Replaced by ``Enquire.matching_terms``, for consistency with
                                              rest of Python API.  Note: an ``Enquire.get_matching_terms`` method existed in
                                              releases up-to and including 1.2.4, but this was actually an old implementation
                                              which only accepted a MSetIterator as a parameter, and would have failed with
                                              code written expecting the version in 1.0.0.  It was fully removed after
                                              release 1.2.4.
------- -------- ---------------------------- --------------------------------------------------------------------------------
1.1.0   SWIG     Error::get_errno()           Use ``Error::get_error_string()`` instead.
        [#rswg]_
------- -------- ---------------------------- --------------------------------------------------------------------------------
1.1.0   SWIG     MSet::get_document_id()      Use ``MSet::get_docid()`` instead.
        [#rsw2]_
------- -------- ---------------------------- --------------------------------------------------------------------------------
1.2.0   Python   mset[i][xapian.MSET_DID] etc This was inadvertently removed in 1.2.0, but not noticed until 1.2.5, by which
                                              point it no longer seemed worthwhile to reinstate it.  Please use the property
                                              API instead, e.g. ``mset[i].docid``, ``mset[i].weight``, etc.
------- -------- ---------------------------- --------------------------------------------------------------------------------
1.2.5   Python   if idx in mset               This was nominally implemented, but never actually worked.  Since nobody seems
                                              to have noticed in 3.5 years, we just removed it.  If you have uses (which were
                                              presumably never called), you can replace them with:
                                              ``if idx >= 0 and idx < len(mset)``
------- -------- ---------------------------- --------------------------------------------------------------------------------
1.3.0   Python   Non-pythonic iterators       Use the pythonic iterators instead.
------- -------- ---------------------------- --------------------------------------------------------------------------------
1.3.0   Python   Stem_get_available_languages Use Stem.get_available_languages instead (static method instead of function)
======= ======== ============================ ================================================================================

.. [#rswg] This affects all SWIG generated bindings (currently: Python, PHP, Ruby, Tcl8 and CSharp)

.. [#rsw2] This affects all SWIG-generated bindings except those for Ruby, support for which was added after the function was deprecated in Xapian-core.

.. [#rsw3] This affects all SWIG generated bindings except those for Ruby, which was added after the function was deprecated in Xapian-core, and PHP, where empty is a reserved word (and therefore, the method remains "is_empty").

.. [#callable] Python handles this like C++.  Ruby renames it to 'call' (idiomatic Ruby).  PHP renames it to 'apply'.  CSharp to 'Apply' (delegates could probably be used to provide C++-like functor syntax, but that's effort and it seems debatable if it would actually be more natural to a C# programmer).  Tcl8 renames it to 'apply' - need to ask a Tcl type if that's the best solution.

Omega
=====

.. Keep table width to <= 126 columns.

======= =================================== ==================================================================================
Removed Feature name                        Upgrade suggestion and comments
======= =================================== ==================================================================================
1.0.0   $freqs                              Use ``$map{$queryterms,$_:&nbsp;$nice{$freq{$_}}}`` instead.
------- ----------------------------------- ----------------------------------------------------------------------------------
1.0.0   scriptindex -u                      ``-u`` was ignored for compatibility with 0.7.5 and earlier, so just remove it.
------- ----------------------------------- ----------------------------------------------------------------------------------
1.0.0   scriptindex -q                      ``-q`` was ignored for compatibility with 0.6.1 and earlier, so just remove it.
------- ----------------------------------- ----------------------------------------------------------------------------------
1.1.0   scriptindex index=nopos             Use ``indexnopos`` instead.
------- ----------------------------------- ----------------------------------------------------------------------------------
1.3.0   ``OLDP`` CGI parameter              Use ``xP`` CGI parameter instead (direct replacement), which has been supported
                                            since at least 0.5.0.
======= =================================== ==================================================================================
