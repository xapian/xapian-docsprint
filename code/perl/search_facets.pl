#!/usr/bin/env perl

use utf8;
use strict;
use warnings;

use JSON::MaybeXS;
use Search::Xapian ':all';
use FindBin qw($Bin);
use lib $Bin;
use Encode qw/decode/;
use Support;
use Data::Dumper;
binmode STDOUT, ":encoding(UTF-8)";
binmode STDERR, ":encoding(UTF-8)";

my ($db_path, @terms) = @ARGV;
die "Usage: $0 DB_PATH QUERY..." unless $db_path && @terms;

search($db_path, join(' ', @terms));

sub search {
    my ($db_path, $query_string, $offset, $pagesize) = @_;
    $offset ||= 0;
    $pagesize ||= 10;
    my $db = Search::Xapian::Database->new($db_path);
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

    # Use an Enquire object on the database to run the query
    my $enquire = $db->enquire($query);

    # And print out something about each match
    my @matches;
    
### Start of example code.

    # Set up a spy to inspect the MAKER value at slot 1
    my $spy = Search::Xapian::ValueCountMatchSpy->new(1);
    $enquire->add_matchspy($spy);

    my $mset = $enquire->get_mset($offset, $pagesize, 100);
    foreach my $item ($mset->items) {
        my $fields = decode_json($item->get_document->get_data);
        printf(q{%i: #%3.3i %s - %s}, $item->get_rank + 1, $item->get_docid, $fields->{TITLE}, $fields->{MAKER});
        print "\n";
        push @matches, $item->get_docid;
    }
    # Fetch and display the spy values
    my $end = $spy->values_end;
    # it looks like the values are not decoded coming out.
    for (my $it = $spy->values_begin; $it != $end; $it++) {
        print "Facet: " . decode('UTF-8', $it->get_termname) . "; count: " . $it->get_termfreq . "\n"
    }


    Support::log_matches($query_string, $offset, $pagesize, \@matches);
### End of example code.
}
