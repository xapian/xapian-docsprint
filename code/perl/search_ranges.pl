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

    # and add in range processors

    # this works with Search::Xapian on debian stable (1.2.24) and cpan (1.2.25)
    # for version in git master, method, classes and constant changed:
    # $queryparser->add_rangeprocessor(Xapian::NumberRangeProcessor->new(0, 'mm', RP_SUFFIX));
    # $queryparser->add_rangeprocessor(Xapian::NumberRangeProcessor->new(1);
    $queryparser->add_valuerangeprocessor(Search::Xapian::NumberValueRangeProcessor->new(0, 'mm', 0));
    $queryparser->add_valuerangeprocessor(Search::Xapian::NumberValueRangeProcessor->new(1));

    # And parse the query
    my $query = $queryparser->parse_query($query_string);

    # Use an Enquire object on the database to run the query
    my $enquire = $db->enquire($query);

    # And print out something about each match
    my @matches;

    my $mset = $enquire->get_mset($offset, $pagesize);
    foreach my $item ($mset->items) {
        my $fields = decode_json($item->get_document->get_data);
        printf(qq{%i: #%3.3i (%s) %s\n        %s\n},
               $item->get_rank + 1,
               $item->get_docid,
               $fields->{DATE_MADE},
               $fields->{MEASUREMENTS},
               $fields->{TITLE});
        push @matches, $item->get_docid;
    }
    Support::log_matches($query_string, $offset, $pagesize, \@matches);
}
