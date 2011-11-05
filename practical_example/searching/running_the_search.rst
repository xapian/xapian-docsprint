Running a Search
----------------
To search the database we're built, you just run our simple search engine::

	$ python search1.py db watch
	1: #004 Watch with Chinese duplex escapement
	2: #018 Solar/Sidereal verge watch with epicyclic maintaining power
	3: #013 Watch timer by P
	4: #033 A device by Favag of Neuchatel which enables a stop watch to
	5: #015 Ingersoll "Dan Dare" automaton pocket watch with pin-pallet
	6: #036 Universal 'Tri-Compax' chronographic wrist watch
	7: #046 Model by Dent of mechanism for setting hands and winding up
	INFO:xapian.search:'watch'[0:10] = 4 18 13 33 15 36 46

These results show that 7 documents match our search for the term
'watch', providing the document IDs (e.g. #004) and title for each.
If you want to search for multiple words, just chain them together on
the command line::

	$ python code/python/search1.py db Dent watch
	1: #046 Model by Dent of mechanism for setting hands and winding up
	2: #004 Watch with Chinese duplex escapement
	3: #018 Solar/Sidereal verge watch with epicyclic maintaining power
	4: #013 Watch timer by P
	5: #094 Model of a Lever Escapement , 1850-1883
	6: #093 Model of Graham's Cylinder Escapement, 1850-1883
	7: #033 A device by Favag of Neuchatel which enables a stop watch to
	8: #015 Ingersoll "Dan Dare" automaton pocket watch with pin-pallet
	9: #086 Model representing Earnshaw's detent chronometer escapement, 1950-1883
	10: #036 Universal 'Tri-Compax' chronographic wrist watch
	INFO:xapian.search:'Dent watch'[0:10] = 46 4 18 13 94 93 33 15 86 36

You'll notice that all of the results from the first time come back
the second time also, with additional ones (the match 'Dent' but not
'watch'), because by default QueryParser will use the OR operator to
combine the different search terms. Also, because #046 contains both
'Dent' and 'watch', it now ranks highest of all the matches.
