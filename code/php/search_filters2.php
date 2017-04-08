<?php
require_once("xapian.php");
require_once("parsecsv.php");
require_once("logger.php");

function search($dbpath, $querystring, $offset = 0, $pagesize = 10)
{
    // offset - defines starting point within result set
    // pagesize - defines number of records to retrieve

    // Open the database we're going to search.
    $db = new XapianDatabase($dbpath);

### Start of example code.
    // Set up a QueryParser with a stemmer and suitable prefixes
    $queryparser = new XapianQueryParser();
    $queryparser->set_stemmer(new XapianStem("en"));
    $queryparser->set_stemming_strategy(XapianQueryParser::STEM_SOME);
    $queryparser->add_prefix("title", "S");
    $queryparser->add_prefix("description", "XD");
    $queryparser->add_boolean_prefix("material", "XM");

    // And parse the query
    $query = $queryparser->parse_query($querystring);
### End of example code.

    // Use an Enquire object on the database to run the query
    $enquire = new XapianEnquire($db);
    $enquire->set_query($query);

    // Retrieve the matches and compute start and end points
    $matches = $enquire->get_mset($offset, $pagesize);
    $match = $matches->begin();
    $end = $matches->end();

    // Use an array to record the DocIds of each match
    $docids = array();

    while (!($match->equals($end)))
    {
        // retrieve the document and its data
        $doc = $match->get_document();
        $fields = json_decode($doc->get_data());
        $position = $match->get_rank() + 1;

        // record the docid
        $docid = $match->get_docid();
        $docids[] = $docid;

        // display the results
        printf("%d: #%3.3d %s\n", $position, $docid, $fields->TITLE);

        // increment MSet iterator and our counter
        $match->next();
    }

    // Finally, make sure we log the query and displayed results
    printf("'%s'[%d:%d] = %s\n",
           $querystring,
           $offset,
           $offset+$pagesize,
           implode(" ", $docids)
    );
}

if ($argc < 2) {
    print "Usage: php $argv[0] DBPATH QUERYTERM...\n";
    die();
}

search($argv[1], join(' ', array_slice($argv, 2)));
?>
