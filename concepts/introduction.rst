==================
Introduction to IR
==================

An information retrieval system retrieves relevant documents based on information need from a document collection.
Generally each *document* is a piece of text, described as collection of *terms*. The *information need* can often be described as a small collection of terms. If you are searching for "golf", the aim of an IR system would be to return all the documents talking about golf.


----------------------------
Indexing: Offline processing
----------------------------

In order to retrieve all the documents with query terms, there are two methods.

* Linear scan of all the documents to see if term is in the document. (Inefficient)
* Offline process all the document in a special format to get list of all document with term for all terms. (Used in IR)

Linear scan is highly inefficient due to scanning of all the document in collection to serve the information need. If you have a lot of documents, it would take huge time to complete such the scan.

In modern information retrieval systems, documents are processed offline to arrange it in special format called an index, in order to avoid having to do linear scans.

Indexing
--------

*Indexing* is the process of converting the documents into a special format for efficient searching and retrieval later. One main component is a list of documents (referenced by document id) in which we can find each term; each list of documents, for a particular term, is called a *posting list*.

| **Documents**

| D[0] = {This is a book}
| D[1] = {Books are worth reading}
| D[2] = {This book is worth buying}

| **Index**

| This - {0,2}
| book - {0,1,2}
| is - {0,2}
| a - {0}
| are - {1}
| worth - {1,2}
| reading - {1}
| buying - {2}

Stemming
--------

Some words are used in their inflected form in the document, for example "connect" can be used as *connecting*, *connected* and *connection*.
Although all the terms (*connecting*, *connected*) are similar, we would not find documents containing "connected" when processing a query for "connect" if we only looked at the posting list of "connect".
Therefore, before we store the term in the index, it is *stemmed* to reduce the inflected word ("connected") to its word stem or root form ("connect").


----------------------------
Retrieval: Online processing
----------------------------

Given a information need, generally given as search query (terms), we try to retrieve relevant documents from the collection using the index formed in the offline processing stage.
There are two major paradigms to retrieving documents.

Boolean Retrieval
-----------------

Boolean retrieval, retrieve the documents by doing union, intersection or difference on the posting lists of terms in the query.

**Posting list of query terms**

| book -> {1,4,10}
| work -> {1,2,4,9}

**Boolean Retrieval**

| book AND work -> {1,4}
| book OR work  -> {1,2,4,9,10}
| book AND_NOT work -> {10}
| work AND_NOT book -> {2,9}

Probabilistic Retrieval
-----------------------

Probabilistic retrieval model is based on the Probability Ranking Principle, which states that an information retrieval system is supposed to rank the documents based on their probability of relevance to the query, given all the evidence available [Belkin and Croft 1992]. The principle takes into account that there is uncertainty in the representation of the information need and the documents. There can be a variety of sources of evidence that are used by the probabilistic retrieval methods, and the most common one is the statistical distribution of the terms in both the relevant and non-relevant documents.


A posting list stores the frequency of terms in different documents, such as in this posting list for the term "work":

| work -> {1:3,2:1,4:2,9:10}

document 1 contains work three times, whereas document id 2 contains it only once.

In probabilistic model we give score to the documents based on frequency of the query words in document.

Query Expansion
---------------

Query expansion is a process where query provided by the user is expanded with extra terms to improve the search results. The aim of query expansion is to generate alternative or expanded queries for the user.
There are two broad approaches to do this:

* Relevance feedback - Users give additional input on documents (by marking documents in the results set as relevant or not), and this input is used to reweight the terms or add new term in the query for documents.
* Pseudo Relevance feedback - top ranking document of the search are considered to be relevant and used to reweight the terms or add new term.


----------
References
----------

* "Information Retrieval" by C. J. van Rijsbergen is well worth reading. It's out of print, but is available for free from the `author's website <http://www.dcs.gla.ac.uk/Keith/Preface.html>`_ (in HTML or PDF).
* "Readings in Information Retrieval" (published by Morgan Kaufmann, edited by Karen Sparck Jones and Peter Willett) is a collection of published papers covering many aspects of the subject.
* "`Managing Gigabytes <http://people.eng.unimelb.edu.au/ammoffat/mg/>`_" (also published by Morgan Kaufmann, written by Ian H. Witten, Alistair Moffat and Timothy C. Bell) describes information retrieval and compression techniques.
* "`Introduction to Information Retrieval <http://www-nlp.stanford.edu/IR-book/>`_" (published by Cambridge University Press, written by Christopher D. Manning, Prabhakar Raghavan and Hinrich) is available both in print and for free online.
* "`Modern Information Retrieval <http://www.mir2ed.org/>`_" (published by Addison Wesley, written by Ricardo Baeza-Yates and Berthier Ribeiro-Neto) gives a good overview of the field. It was published more recently than the books above, and so covers some more recent developments.
