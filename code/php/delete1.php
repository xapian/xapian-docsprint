<?php
require_once("xapian.php");

// Start of example code.
function delete1 ($dbpath, $identifiers)
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
    print "Usage: php delete1.php <db_path> <identifier>...\n";
    die();
}

// Call the index function.
delete1($argv[1], array_slice($argv, 2));
?>
