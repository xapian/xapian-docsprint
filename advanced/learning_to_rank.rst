
.. Copyright (C) 2011 Parth Gupta
.. Copyright (C) 2016 Ayush Tomar


=======================
Xapian Learning-to-Rank
=======================

.. contents:: Table of Contents


Introduction
============

Learning-to-Rank(LTR) can be viewed as a weighting scheme which involves machine learning. The main idea behind LTR is to bring up relevant documents given a low ranking by probablistic techniques like BM25 by using machine learning models. A model is trained by learning from the relevance judgements provided by a user corresponding to a set of queries and a corpus of documents. This model is then used to re-rank the matchset to bring more relevant documents higher in the ranking. Learning-to-Rank has gained immense popularity and attention among researchers recently.

LTR can be broadly seen in two stages: Learning the model and Ranking. Learning the model takes the training file as input and produces a model. After that given this learnt model, when a new query comes in, scores can be assigned to the documents associated to it.

Preparing the Training file
---------------------------

Currently the ranking models supported by LTR are supervised learning models. A supervised learning model requires a labelled training data as an input. To learn a model using LTR you need to provide the training data in the following format.

.. code-block:: none

    0 qid:10032 1:0.130742 2:0.000000 3:0.333333 4:0.000000 ... 18:0.750000 19:1.000000 #docid = 1123323
    1 qid:10032 1:0.593640 2:1.000000 3:0.000000 4:0.000000 ... 18:0.500000 19:0.023400 #docid = 4222333

Here each row represents the document for the specified query. The first column is the relevance label and which can take non-negative values. The second column represents the queryid, and the last column is the docid. The third column represents the value of the features.

As mentioned before, this process requires a training file in the above format. xapian-letor API empowers you to generate such training file. But for that you have to supply some information like:

1. Query file: This file has information of queries to be involved in
   learning and its id. It should be formatted in such a way::

    2010001 'landslide,malaysia'
    2010002 'search,engine'
    2010003 'Monuments,of,India'
    2010004 'Indian,food'

   where 2010xxx being query-id followed by a comma separated query in
   single-quotes.

2. Qrel file: This is the file containing relevance judgements. It should
   be formatted in this way::

    2010003 Q0 19243417 1
    2010003 Q0 3256433 1
    2010003 Q0 275014 1
    2010003 Q0 298021 0
    2010003 Q0 1456811 0

   where first column is query-id, third column is Document-id and fourth column being relevance label which is 0 for irrelevance and 1 for relevance. Second column is many times referred as 'iter' but doesn't really important for us.  All the fields are whitespace delimited. This is the standard format of almost all the relevance judgement files. If you have relevance judgements in a different format then you can convert it to this format using a text processing tool such as 'awk'.

3. Collection Index : Here you supply the path to the index of the corpus. If
   you have 'title' information in the collection with some xml/html tag or so
   then add::

    indexer.index(title,1,"S");

You can refer to the "Indexing" section under "A practical example" heading for the Collection Index. The database created in the practical example will be used as the collection index for the examples. In particular we are going to be using all the documents which contain the term "watch", which will be used as the query for the examples.

Provided such information, API is capable of creating the training file which is in the mentioned format and can be used for learning a model.

To prepare a training file run the following command from the top level directory. This example assumes that you have created the db from the first example in "Indexing" section under "A practical example" header and you have installed xapian-letor.

.. code-block:: none

    $ xapian-prepare-trainingfile --db=db data/query.txt data/qrel.txt training_data.txt

xapian-prepare-trainingfile is a utility present after you have installed xapian-letor. This should create a training_data.txt which should have the similar values to the data/training_data.txt.

The source code is present for xapian-prepare-trainingfile.cc is present at `xapian/xapian-letor/bin/xapian-prepare-trainingfile.cc <https://github.com/xapian/xapian/blob/master/xapian-letor/bin/xapian-prepare-trainingfile.cc>`_.

Learning the Model
------------------

In xapian-letor we support the following learning algorithms:

1. `ListNET <http://dl.acm.org/citation.cfm?id=1273513>`_
2. `Ranking-SVM <http://dl.acm.org/citation.cfm?id=775067>`_
3. `ListMLE <http://icml2008.cs.helsinki.fi/papers/167.pdf>`_

You can use any one of the rankers to Learn the model. The command line tool xapian-train uses ListNET as the ranker for learning. To learn a model run the following command from the top level directory.

.. code-block:: none

    $ xapian-train --db=db data/training_data.txt "ListNET_Ranker"

Ranking
-------

After we have built a model, it's quite straightforward to get a real score for a particular document for the given query. Here we supply the first hand retrieved ranked-list to the Ranking function, which assigns a new score to each document after converting it to the same dimensioned feature vector. This list is re-ranked according to the new scores.

Here’s the significant part of the example code to implement ranking.

.. xapianexample:: search_letor

A full copy of this code is available in :xapian-code-example:`^`

You can run this code as follows to re-rank the list of documents retrieved from the db containing the term "watch" in the order of relevance as mentioned in the data/qrel.

.. xapianrunexample:: index1
    :silent:
    :args: data/100-objects-v1.csv db

.. xapiantrain:: search_letor

.. xapianrunexample:: search_letor
    :args: db ListNET_Ranker watch
    :letor:

Features
========

Features play a major role in the learning. In LTR, features are mainly of three types: query dependent, document dependent (pagerank, inLink/outLink number, number of children, etc) and query-document pair dependent (TF-IDF Score, BM25 Score, etc).

Currently we have incorporated 19 features which are described below. These features are statistically tested in `Nallapati2004 <http://dl.acm.org/citation.cfm?id=1009006>`_.

    Here c(w,D) means that count of term w in Document D. C represents the Collection. 'n' is the total number of terms in query.
    :math:`|.|` is size-of function and idf(.) is the inverse-document-frequency.


    1. :math:`\sum_{q_i \in Q \cap D} \log{\left( c(q_i,D) \right)}`

    2. :math:`\sum_{i=1}^{n}\log{\left(1+\frac{c\left(q_i,D\right)}{|D|}\right)}`

    3. :math:`\sum_{q_i \in Q \cap D} \log{\left(idf(q_i) \right) }`

    4. :math:`\sum_{q_i \in Q \cap D} \log{\left( \frac{|C|}{c(q_i,C)} \right)}`

    5. :math:`\sum_{i=1}^{n}\log{\left(1+\frac{c\left(q_i,D\right)}{|D|}idf(q_i)\right)}`

    6. :math:`\sum_{i=1}^{n}\log{\left(1+\frac{c\left(q_i,D\right)}{|D|}\frac{|C|}{c(q_i,C)}\right)}`


All the above 6 features are calculated considering 'title only', 'body only' and 'whole' document. So they make in total 6*3=18 features. The 19th feature is the Xapian weighting scheme score assigned to the document (by default this is BM25).The API gives a choice to select which specific features you want to use. By default, all the 19 features defined above are used.

One thing that should be noticed is that all the feature values are `normalized at Query-Level <https://trac.xapian.org/wiki/GSoC2011/LTR/Notes#QueryLevelNorm>`_. That means that the values of a particular feature for a particular query are divided by its query-level maximum value and hence all the feature values will be between 0 and 1. This normalization helps for unbiased learning.

Nallapati, R. Discriminative models for information retrieval. Proceedings of SIGIR 2004 (pp. 64-71).
