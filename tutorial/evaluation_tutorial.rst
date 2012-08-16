Tutorial to configure evaluation module in xapian
=================================================

 Evaluation module is one of essential module for a search engine to be used in academia.This module ease to calculate various metric  precision, recall, precision @ rank,Precision @ recall which validates implementation and check the engine on result presented on literature.xapian being an open source engine have implemented evaluation module to help people from academia.

Using Evaluation Module
------------------------

Evaluation metric currently in xapian
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

 * Mean Average precision(MAP)
 * Mean Relevance Precision(MRP)
 * Precision at Rank
 * Precision at Recall
 * Recall

Indexing Collection with evaluation Module.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

User can index a collection using
::
 . ./trec_index configuration_file

User need to compulsary configure textfile,db,stopfile parameters to be able to use index a collection.User need to set indexbigram parameter to true to be able to index bigrams while indexing to use bigram language model weighting scheme.

Searching Topics file and creating run with evaluation module
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

User can search a collection using index build to create a run with queries in topic file.
::
 ./trec_query configuration_file;
 ./trec_search configuration_file

User need to compulsary configure queryfile ,topicfile, stopfile to search using a topic file,needs to set queryparserbigram to true to be able to add bigrams in query object formed by bigram.

Evaluating the run.
^^^^^^^^^^^^^^^^^^^

User need to run to get the evaluation result for your run.
::
 ./trec_adhoceval configuration_file

Its compulsary to set relfile,runfile for using this option.

Configuring evaluation module
------------------------------

Configurable Parameters:
^^^^^^^^^^^^^^^^^^^^^^^^

	 - textfile     - path/filename of text file to be indexed for evaluation
	 - language     - corpus language to be indexed for stemming 
	 - db           - path of database which is index of above textfile
	 - querytype    - type of query
	 - queryfile    - path/filename of query file to be ran and searched
	 - resultsfile  - path/filename of results file(run file)
	 - transfile    - path/filename of transaction file
	 - noresults    - no of results to save in results log file
	 - const_k1     - value for K1 constant (BM25)
	 - const_b      - value for B constant (BM25)
	 - topicfile    - path/filename of topic file for which relevance judgement file is available
	 - topicfields  - fields of topic to use from topic file in evaluation
	 - relfile      - path/filename of relevance judgements file
	 - runname      - name of the evaluation run
	 - nterms       - no of terms to pick from the topic
	 - stopsfile    -  name of the stopword file
	 - evaluationfiles - path/filename of the evaluation files(where evaluation result is stored).
	 - indexbigram  - Index Bigram in the index.
	 - queryparsebigram -  Parse and add bigrams to the Query.
	 - weightingscheme - which weighting scheme to select(bm25,lmweight,trad,boolweight)

Parameters to be configured using for BM25 Weighting Scheme
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
**All parameter need to be configured to call customized constructor.Please refer generated documentation for value of parameters. at http://xapian.org/docs/**

	 - bm25param_k1
	 - bm25param_k2
	 - bm25param_k3
	 - bm25param_b
	 - bm25param_min_normlen
	
Parameters for Tras Weighting scheme.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

	 - tradparam_k

Parameters for LMWeight Weighting Scheme
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**All parameters need to be configured to call customized constructor.Please refer generated docs for value of parameter at http://xapian.org/docs/**

	 - lmparam_log
	 - lmparam_smoothing1
	 - lmparam_smoothing2
	 - lmparam_mixture
     - lmparam_select_smoothing
