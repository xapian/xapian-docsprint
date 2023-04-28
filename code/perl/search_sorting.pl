#!/usr/bin/env perl

use strict;
use warnings;

BEGIN {
  eval {
    require Xapian;
    Xapian->import(':all');
    Xapian::search_xapian_compat();
  };
  if ($@) {
    require Search::Xapian;
    Search::Xapian->import(':all');
  }
}

use JSON::MaybeXS;
use FindBin qw($Bin);
use lib $Bin;
use Support;


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

    # Start of example code.
    $enquire->set_sort_by_value_then_relevance(1, 0);
    # End of example code.


    # And print out something about each match
    my @matches;
    
    my $mset = $enquire->get_mset($offset, $pagesize);
    foreach my $item ($mset->items) {
        my $fields = decode_json($item->get_document->get_data);
        printf(qq{%i: #%3.3i %s %s\n        Population %s\n},
               $item->get_rank + 1,
               $item->get_docid,
               $fields->{name},
               Support::format_date($fields->{admitted}),
               Support::format_numeral($fields->{population}));
        push @matches, $item->get_docid;
    }
    Support::log_matches($query_string, $offset, $pagesize, \@matches);
}

