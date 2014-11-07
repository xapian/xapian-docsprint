<?php
require_once("xapian.php");

// Start of example code.
function delete_docs ($dbpath, $identifiers)
{
    // Open the database we're going to be deleting from.
    $db = new XapianWritableDatabase($dbpath, Xapian::DB_OPEN);

    foreach ($identifiers as $identifier)
    {
        $idterm = 'Q' . $identifier;
        $db->delete_document($idterm);
    }
}
// End of example code.

if ($argc < 3) {
    print "Usage: php $argv[0] DBPATH ID...\n";
    die();
}

// Call the delete_docs function.
delete_docs($argv[1], array_slice($argv, 2));
?>
