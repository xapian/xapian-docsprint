Diversification of Search Results
=================================

.. contents:: Table of contents

Introduction
------------

Xapian allows for diversification of documents which are stored in the form of an MSet.
This feature is a well-known technique in information retrieval used to increase
user satisfaction, especially for ambiguous queries.

Xapian currently has an implementation of an *implicit* method (using documents as features,
as opposed to using query based features such as query logs) adapted from the C :sup:`2` - GLS method mentioned in Scalable and Efficient Web Search Results Diversification, Naini et al. 2016. This saves the cost of having to provide external features such as query
logs, while still achieving the desired diversification effect, which according to
the paper is reasonable enough for practical uses as tested on the public data set - ClueWeb09 with TREC Web 09/10 queries.

API
---
 
Diversification on an MSet of results can be achieved by using the
:xapian-class:`Diversify` class, e.g.::

    // Query a database and get 10 results, where 'enq' is an instantiated
    // Enquire object over a database
    matches = enq.get_mset(0, 10)

Now, cluster the 10 candidate documents into 4 clusters and use (at most) top-2
documents from each cluster for diversification::    
    
    k, r = 4, 2
    // Instantiate Diversify object
    d = xapian.Diversify(k, r)

Perform diversification over 'matches' and obtain an ordered list of documents::

    dset = d.get_dmset(matches)
