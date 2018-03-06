#!/usr/bin/env perl

use strict;
use warnings;

use JSON::MaybeXS;
use Search::Xapian ':all';
use FindBin qw($Bin);
use lib $Bin;
use Support;


my ($db_path, @terms) = @ARGV;
die "Usage: $0 DB_PATH QUERY..." unless $db_path && @terms;

search($db_path, join(' ', @terms));

### Start of example code.
sub search {
    my ($db_path, $query_string, $offset, $pagesize) = @_;
    $offset ||= 0;
    $pagesize ||= 10;
    my $db = Search::Xapian::WritableDatabase->new($db_path, DB_OPEN);

    # Start of adding synonyms    
    $db->add_synonym(time => 'calendar');
    # End of adding synonyms

    # Set up a QueryParser with a stemmer and suitable prefixes
    my $queryparser = Search::Xapian::QueryParser->new;
    $queryparser->set_stemmer(Search::Xapian::Stem->new('en'));
    $queryparser->set_stemming_strategy(STEM_SOME);

    # Start of prefix configuration.
    $queryparser->add_prefix(title => "S");
    $queryparser->add_prefix(description => "XD");
    # End of prefix configuration.

    # Start of set database
    $queryparser->set_database($db);
    # End of set database

    # And parse the query
    my $query = $queryparser->parse_query($query_string, FLAG_SYNONYM);

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
### End of example code.
