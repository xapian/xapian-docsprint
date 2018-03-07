#!/usr/bin/env perl

use strict;
use warnings;

use JSON::MaybeXS;
use Search::Xapian ':all';
use FindBin qw($Bin);
use lib $Bin;
use Support;
use Data::Dumper;


my ($db_path, $query_string, @materials) = @ARGV;
die "Usage: $0 DB_PATH QUERY MATERIALS..." unless $db_path && $query_string;

search($db_path, $query_string, \@materials);

sub search {
    my ($db_path, $query_string, $materials, $offset, $pagesize) = @_;
    $materials ||= [];
    $offset    ||= 0;
    $pagesize  ||= 10;

    my $db = Search::Xapian::Database->new($db_path);

### Start of example code.
    # Set up a QueryParser with a stemmer and suitable prefixes
    my $queryparser = Search::Xapian::QueryParser->new;
    $queryparser->set_stemmer(Search::Xapian::Stem->new('en'));
    $queryparser->set_stemming_strategy(STEM_SOME);

    # Start of prefix configuration.
    $queryparser->add_prefix(title => "S");
    $queryparser->add_prefix(description => "XD");

    # End of prefix configuration.

    # And parse the query
    my $query = $queryparser->parse_query($query_string);

    # there is no pod for Search::Xapian::Query, but works anyway. Operator + list.

    if (@$materials) {
        my $material_query = Search::Xapian::Query->new(OP_OR,
                                                        map { Search::Xapian::Query->new('XM' . lc($_)) }
                                                        @$materials);
        $query = Search::Xapian::Query->new(OP_FILTER, $query, $material_query);
    }
### End of example code.
    
    # Use an Enquire object on the database to run the query
    my $enquire = $db->enquire($query);

    # And print out something about each match
    my @matches;
    
    my $mset = $enquire->get_mset($offset, $pagesize);
    foreach my $item ($mset->items) {
        my $fields = decode_json($item->get_document->get_data);
        printf(q{%i: #%3.3i %s}, $item->get_rank + 1, $item->get_docid, $fields->{TITLE});
        print "\n";
        push @matches, $item->get_docid;
    }
    Support::log_matches($query_string, $offset, $pagesize, \@matches);
}
