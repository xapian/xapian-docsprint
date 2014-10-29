<?php
require_once("xapian.php");
require_once("parsecsv.php");
require_once("logger.php");

## Start of example code.
function search($dbpath, $querystring, $offset = 0, $pagesize = 10)
{
    // offset - defines starting point within result set
    // pagesize - defines number of records to retrieve

    // Open the database we're going to search.
    $db = new XapianDatabase($dbpath);

    // Set up a QueryParser with a stemmer and suitable prefixes
    $queryparser = new XapianQueryParser();
    $queryparser->set_stemmer(new XapianStem("english"));
    $queryparser->set_stemming_strategy(XapianQueryParser::STEM_SOME);
    // Start of prefix configuration.
    $queryparser->add_prefix("title", "S");
    $queryparser->add_prefix("description", "XD");
    // End of prefix configuration.

    // And parse the query
    $query = $queryparser->parse_query($querystring);

    // Use an Enquire object on the database to run the query
    $enquire = new XapianEnquire($db);
    $enquire->set_query($query);

    // Retrieve the matches and compute start and end points
    $matches = $enquire->get_mset($offset, $pagesize);
    $start = $matches->begin();
    $end = $matches->end();
    $index = 0;

    // Use an array to record the DocIds of each match
    $docids = array();

    while (!($start->equals($end)))
    {
        // retrieve the document and its data
        $doc = $start->get_document();
        $fields = json_decode($doc->get_data());
        $position = $offset + $index + 1;

        // record the docid
        $docid = $start->get_docid();
        $docids[] = $docid;

        // display the results
        print sprintf("%d: #%03d %s\n", $position, $docid, $fields->TITLE);

        // increment MSet iterator and our counter
        $start->next();
        $index++;
    }

    // Finally, make sure we log the query and displayed results
    log_info(sprintf("xapian.search:'%s'[%d:%d] = %s",
                $querystring,
                $offset,
                $offset+$pagesize,
                implode(" ", $docids)
            ));
}
## End of example code.

if ($argc != 3) {
    print "Usage: php search1.php <db_path> <query_string>\n";
    die();
}

search($argv[1], $argv[2]);
?>
