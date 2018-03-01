#!/usr/bin/env perl

use utf8;
use strict;
use warnings;
use Encode qw/decode encode is_utf8/;
use Test::More;
use File::Temp;
use Search::Xapian ':all';

my $decoded_string = "Đe ši Šu";
my $encoded_string = encode('UTF-8', $decoded_string);
# most misnamed function ever, and it's internal anyway. Should be is_decoded()
ok is_utf8($decoded_string), "decode is decoded";
ok !is_utf8($encoded_string), "encoded is encoded";
isnt $decoded_string, $encoded_string, "Strings differ";

my $tmp = File::Temp->newdir;
my $db_path = $tmp->dirname;

foreach my $store_encoded (0..1) {
    # index
    {
        my $db = Search::Xapian::WritableDatabase->new($db_path, DB_CREATE_OR_OPEN);
        my $term_generator = Search::Xapian::TermGenerator->new;
        $term_generator->set_stemmer(Search::Xapian::Stem->new('none'));
        my $doc = Search::Xapian::Document->new;
        $term_generator->index_text('try');

        # this is the gist of the demostration. It doesn't care if the
        # encoding string is encoded or decoded. We always get back
        # the encoded one.
        if ($store_encoded) {
            $doc->set_data($encoded_string);
            $doc->add_value(0, $encoded_string);
        }
        else {
            $doc->set_data($decoded_string);
            $doc->add_value(0, $decoded_string);
        }

        my $id = 'Qtry1';
        $doc->add_boolean_term($id);
        $db->replace_document_by_term($id, $doc);
    }
    # search and test
    {
        my $db = Search::Xapian::Database->new($db_path);
        my $query = Search::Xapian::Query->new('Qtry1');
        my $enquire = $db->enquire($query);
        my ($res) = $enquire->get_mset(0, 1)->items;
        my $doc = $res->get_document;
        is $doc->get_data, $encoded_string;
        isnt $doc->get_data, $decoded_string, "data is binary";
        is $doc->get_value(0), $encoded_string;
        isnt $doc->get_value(0), $decoded_string, "value is binary as well";
    }
}

done_testing;
