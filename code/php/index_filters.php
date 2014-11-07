<?php
require_once("xapian.php");
require_once("parsecsv.php");

// Start of example code
function index ($datapath, $dbpath)
{
    // Create or open the database we're going to be writing to.
    $db = new XapianWritableDatabase($dbpath, Xapian::DB_CREATE_OR_OPEN);

    // Set up a TermGenerator that we'll use in indexing
    $termgenerator = new XapianTermGenerator();
    $termgenerator->set_stemmer(new XapianStem('en'));

    // open the file
    $fH = open_file($datapath);

    //    Read the header row in
    $headers = get_csv_headers($fH);

    while (($row = parse_csv_row($fH, $headers)) !== false) {
        // mapping from field name to value using first row headers
        // We're just going to use id_NUMBER, TITLE and DESCRIPTION
        $description = $row['DESCRIPTION'];
        $title       = $row['TITLE'];
        $identifier  = $row['id_NUMBER'];
        $collection  = $row['COLLECTION'];
        $maker       = $row['MAKER'];

        // we make a document and tell the term generator to use this
        $doc = new XapianDocument();
        $termgenerator->set_document($doc);

        // index each field with a suitable prefix
        $termgenerator->index_text($title, 1, 'S');
        $termgenerator->index_text($description, 1, 'XD');

        // index fields without prefixes for general search
        $termgenerator->index_text($title);
        $termgenerator->increase_termpos();
        $termgenerator->index_text($description);

        ### Start of new indexing code.
        // index the MATERIALS field, splitting on semicolons
        $materials = explode(";", $row['MATERIALS']);
        foreach ($materials as $material)
        {
            $material = strtolower(trim($material));
            if ($material != '')
            {
                $doc->add_boolean_term('XM'.$material);
            }
        }
        ### End of new indexing code.

        // store all the fields for display purposes
        $doc->set_data(json_encode($row));

        // we use the identifier to ensure each object ends up
        // in the database only once no matter how many times
        // we run the indexer
        $idterm = "Q".$identifier;
        $doc->add_term($idterm);
        $db->replace_document($idterm, $doc);
    }
}
// End of example code

if ($argc != 3) {
    print "Usage: php $argv[0] DATAPATH DBPATH\n";
    die();
}

// call the index function
index($argv[1], $argv[2]);
?>
