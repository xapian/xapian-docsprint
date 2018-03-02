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

sub index_csv {
    my ($data_path, $db_path) = @_;
    # Create or open the database we're going to be writing to.
    my $db = Search::Xapian::WritableDatabase->new($db_path, DB_CREATE_OR_OPEN);
    # Set up a TermGenerator that we'll use in indexing.
    my $term_generator = Search::Xapian::TermGenerator->new;
    $term_generator->set_stemmer(Search::Xapian::Stem->new('en'));
    foreach my $rec (Support::parse_csv($data_path)) {
        # print Dumper($rec);
        my $doc = Search::Xapian::Document->new;
        $term_generator->set_document($doc);
        # Index each field with a suitable prefix.
        $term_generator->index_text($rec->{TITLE}, 1, 'S');
        $term_generator->index_text($rec->{DESCRIPTION}, 1, 'XD');

        ### Start of new indexing code.
        # Index the MATERIALS field, splitting on semicolons.
        foreach my $material (split(/;/, $rec->{MATERIALS})) {
            $material =~ s/\A\s*//;
            $material =~ s/\z\s*//;
            $material = lc($material);
            if (length($material)) {
                $doc->add_boolean_term('XM' . $material);
            }
        }
        ### End of new indexing code.

        # Index fields without prefixes for general search.
        $term_generator->index_text($rec->{TITLE});
        $term_generator->increase_termpos();
        $term_generator->index_text($rec->{DESCRIPTION});

        # Store all the fields for display purposes.
        $doc->set_data(encode_json($rec));

        # We use the identifier to ensure each object ends up in the
        # database only once no matter how many times we run the
        # indexer.
        my $idterm = "Q" . $rec->{id_NUMBER};
        $doc->add_boolean_term($idterm);
        $db->replace_document_by_term($idterm, $doc);
    }
}

