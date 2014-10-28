==================
Introduction to IR
==================

Information retrieval system retrieves relevent documents based on information need  from a document collection. 
Generally document is a piece of text, described as collection of terms. Information need can often be described as collection of few terms. If you are searching for  "golf", Aim of an IR system would be to return all the document containing golf.


----------------------------
Indexing: Offline processing
----------------------------

In order to retrieve all the document with query terms, there are two methods.
* Linear scan of all the documents to see if term is in the document. (Inefficient)
* Offline process all the document in a special format to get list of all document with term for all terms. (Used in IR)

Linear scan is highly inefficient due to scanning of  all the docuemnt in collection to serve the information need. It would take huge time to return document.

In modern information retrieval systems, documents are processed offline to arrange it in special format called index to avoid linear scan. Special format is index.

Indexing
--------

Indexing is a process of converting the text documents into a special format(index) for efficient retrieval of document.
It's a list of documents(referenced by document id) containing particular term, it is know as posting list.

| **Documents:**

| D[0] = {This is a book}
| D[1] = {Books are worth reading}
| D[2] = {This book is worth buying}

| **Index:**

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

Some words are used in there inflected form in the document, for example connect can be used as connecting, connected , connection . 
Since all the terms(connecting, connected) are similar, but as per design of index, we will not get documents containing connected with query  connect using posting list of connect.
Therefore before we store the term in index, term is stemmed to reduce the inflected word to their word stem form or root form.
For example buying will be stored as buy in the index.


-----------------------------
Retrieval: Online processing
-----------------------------

Given a information need, generally given as search query (terms), we try to retrieve relevant documents from the collection using the index formed in the offline processing stage.
There are two major paradigm to retrieve document.
* Boolean Retrieval

Boolean retrieval, retrieve the documents by doing union, intersection or difference  on the posting list of terms in the query.

**Posting list of query term's:**

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


Posting list stores the frequency of occurance of word in document.
Posting list for work:

| work -> {1:3,2:1,4:2,9:10}

document 1 contains work 3 times, where as document id 2 constains 1 time.

In probabilistic model we give score to the documents based on frequency of the query words in document.

Query Expansion:
----------------

Query expansion is a process where query provided by the user is expanded with extra terms to improve the search results. Aim of query expansion is to generate alternative or expanded queries for the user.
There are two broad approaches to do this:
* Relevance feedback - Users give additional input on documents (by marking documents in the results set as relevant or not), and this input is used to reweight the terms or add new term in the query for documents.
* Pseudo Relevance feeback  -  Top ranking document of the search are considered to be relevant and used to reweight the terms or add new term.


References:
-----------
* "Information Retrieval" by C. J. van Rijsbergen is well worth reading. It's out of print, but is available for free from the author's website (in HTML or PDF).
* "Readings in Information Retrieval" (published by Morgan Kaufmann, edited by Karen Sparck Jones and Peter Willett) is a collection of published papers covering many aspects of the subject.
* "Managing Gigabytes" (also published by Morgan Kaufmann, written by Ian H. Witten, Alistair Moffat and Timothy C. Bell) describes information retrieval and compression techniques.
* "Modern Information Retrieval" (published by Addison Wesley, written by Ricardo Baeza-Yates and Berthier Ribeiro-Neto) gives a good overview of the field. It was published more recently than the books above, and so covers some more recent developments.
* Introduction to Information Retrieval (published by Cambridge University Press, written by Christopher D. Manning, Prabhakar Raghavan and Hinrich )
