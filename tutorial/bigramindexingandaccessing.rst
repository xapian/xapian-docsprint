Tutorial to Index Bigram and access Bigrams,Bigram Postings
==============================================================

Brass backend now support bigram indexing and use it for facilitating Language Model Search.
Bigrams usage can be extended by using them as collocation for Diversified Search results,query reformulation suggestions etc.

Introduction to Bigram:
-------------------------

A bigram or digram is every sequence of two adjacent elements in a string of tokens:  
::
	Document Content:

	Read a book about the history of read.
	
	Correponding Bigrams(with Stop words removal):
	read book
	book about
	about history
	history read

Enabling Bi-gram Indexing in Xapian
-----------------------------------

API User need to call set_bigram method with argument true to enable bigram indexing:
::
	   indexer.set_bigrams(true);

**Caution:**

It is advisable to API User to set a stop word list using Stopper class, Since indexing Bigram without removing stop words will ruin the statistics of Bigram and might result in decreased performance.

Access to Bi-gram
------------------

Since Bi-grams from the document are stored in document object.It is possible to add,remove the Bi-grams from the document object.
Document provide following methods to API user to access bigrams and alter bigrams.

API Function to Access and Alter Bi-grams at Document Level
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Document object allow API User to Add,Remove,Clear and Iterate over the list of bigrams:
::	

	Xapian::Document doc;
	doc.set_data("");
	doc.add_bigram("read book",2); //Adding bigrams to document object
	doc.remove_bigram("read book"); //Removing bigram from document object
	doc.clear_bigrams(); // Remove all bigrams from document object.
	doc.add_bigram("about history",1);
	doc.add_bigram("read book",1);
	Xapian::BigramIterator bi = doc.bigramlist_begin();//Creating iterator for bigram list of document.
	while( bi != doc.bigramlist_end())
	{
	cout<<*bi; // print the bigram for the current position
	bi++; //Increment bigram Itertor to next position
	}
	
Above example almost cover all function provided by document object to access,alter bigram(Refer to Documentation for exact syntax of API.


Accessing TermList of Document from Backend
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Database provide direct access to the bigram list of the document and the posting list of the particular bigram for document aand bigram stored in backend respectively.
API User can iterate over the bigram list of a document using BigramIterator:
::
	databaseobject.bigramlist_begin(Xapian::docid did);

You can iterate over list in way similar to desribed above for posting iterator.

Accessing Posting List of Bi-gram
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

User can iterate over the document id of document which index the particular bigram using PostingIterator:
::
	databaseobject.postlistbigram_begin(const std::string &bname);

Accessing List of All Bigrams in Backend
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Iterating over all the Bi-gram present in the backend using BigramIterator:
::
	databaseobject.allbigrams_begin();

Brass backend provide a full support to index bigrams from the document and access bigram and posting list of bigrams from backend.
