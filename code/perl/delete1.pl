#!/usr/bin/env perl

use strict;
use warnings;
use Search::Xapian ':all';

my ($db_path, @ids) = @ARGV;
die "Usage $0 DBPATH ID..." unless $db_path && @ids;

delete_docs($db_path, @ids);

### Start of example code.
sub delete_docs {
    my ($db_path, @ids) = @_;
    my $db = Search::Xapian::WritableDatabase->new($db_path, DB_CREATE_OR_OPEN);
    foreach my $id (@ids) {
        $db->delete_document_by_term("Q$id");
    }
}
### End of example code.
