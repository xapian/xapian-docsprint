#!/usr/bin/env perl

use strict;
use warnings;

use JSON::MaybeXS;
use Search::Xapian ':all';
use FindBin qw($Bin);
use lib $Bin;
use Support;
use Data::Dumper;

my ($data_path, $db_path) = @ARGV;
die "Usage $0 DATAPATH DBPATH" unless $data_path && $db_path;

index_csv($data_path, $db_path);

### Start of example code.
sub index_csv {
    my ($data_path, $db_path) = @_;
    # Create or open the database we're going to be writing to.
    my $db = Search::Xapian::WritableDatabase->new($db_path, DB_CREATE_OR_OPEN);
    # Set up a TermGenerator that we'll use in indexing.
    my $term_generator = Search::Xapian::TermGenerator->new;
    $term_generator->set_stemmer(Search::Xapian::Stem->new('en'));
    foreach my $rec (Support::parse_states($data_path)) {
        my $doc = Search::Xapian::Document->new;
        $term_generator->set_document($doc);

### Start of example code.
        # Index each field with a suitable prefix.
        $term_generator->index_text($rec->{name}, 1, 'S');
        $term_generator->index_text($rec->{description}, 1, 'XD');
        $term_generator->index_text($rec->{motto}, 1, 'XD');

        # Index fields without prefixes for general search.
        $term_generator->index_text($rec->{name});
        $term_generator->increase_termpos();
        $term_generator->index_text($rec->{description});
        $term_generator->increase_termpos();
        $term_generator->index_text($rec->{motto});

        if (length($rec->{admitted})) {
            $doc->add_value(1, Search::Xapian::sortable_serialise(substr($rec->{admitted}, 0, 4)));
            $doc->add_value(2, $rec->{admitted});
        }
        if (length($rec->{population})) {
            $doc->add_value(3, Search::Xapian::sortable_serialise(int($rec->{population})));
        }
### End of example code.

        # Store all the fields for display purposes.
        $doc->set_data(encode_json($rec));

        # We use the identifier to ensure each object ends up in the
        # database only once no matter how many times we run the
        # indexer.
        my $idterm = "Q" . $rec->{order};
        $doc->add_boolean_term($idterm);
        $db->replace_document_by_term($idterm, $doc);
    }
}
### End of example code.
