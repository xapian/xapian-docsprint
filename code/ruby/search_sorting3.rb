#!/usr/bin/env ruby
# frozen_string_literal: true

require 'xapian'
require 'json'
require_relative 'support'

    # Start of example code.
class DistanceKeyMaker < Xapian::KeyMaker
  def __call__(doc)
    coords = doc.value(4).split(',').map(&:to_f)
    washington = [38.012, -77.037]
    Xapian.sortable_serialise(distance_between_coords(coords, washington))
  end
end
## and later
# enquire.set_sort_by_key_then_relevance(DistanceKeyMaker.new, false)
    # End of example code.

def search(dbpath, querystring, offset: 0, pagesize: 10)
  # offset - defines starting point within result set
  # pagesize - defines number of records to retrieve

  # Open the database we're going to search.
  db = Xapian::Database.new(dbpath)

  # Set up a QueryParser with a stemmer and suitable prefixes
  queryparser = Xapian::QueryParser.new
  queryparser.stemmer = Xapian::Stem.new('en')
  queryparser.stemming_strategy = Xapian::QueryParser::STEM_SOME
  queryparser.add_prefix('title', 'S')
  queryparser.add_prefix('description', 'XD')

  # And parse the query
  query = queryparser.parse_query(querystring)

  # Use an Enquire object on the database to run the query
  enquire = Xapian::Enquire.new(db)
  enquire.query = query

  enquire.set_sort_by_key_then_relevance(DistanceKeyMaker.new, false)

  # And print out something about each match
  matches = []
  enquire.mset(offset, pagesize).matches.each do |match|
    fields = JSON.parse(match.document.data)
    printf "%<rank>i: #%<docid>3.3i %<name>s %<date>s\n        Population %<pop>s\n",
           rank: match.rank + 1,
           docid: match.docid,
           name: fields['name'],
           date: format_date(fields['admitted'].to_s),
           pop: format_numeral(fields['population'].to_i),
           lat: fields['latitude'].to_s,
           lon: fields['longitude'].to_s

    matches << match.docid
  end
  # Finally, make sure we log the query and displayed results
  log_matches(querystring, offset, pagesize, matches)
end

abort "Usage #{__FILE__} DBPATH QUERY..." if ARGV.length < 2

search(ARGV[0], ARGV[1..].join(' '))
