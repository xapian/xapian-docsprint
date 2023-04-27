#!/usr/bin/env ruby
# frozen_string_literal: true

require 'xapian'
require 'json'
require_relative 'support'

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

  # And print out something about each match
  matches = []

### Start of example code.
  # Set up a spy to inspect the MAKER value at slot 1
  spy = Xapian::ValueCountMatchSpy.new(1)
  enquire.add_matchspy(spy)

  enquire.mset(offset, pagesize, 100).matches.each do |match|
    fields = JSON.parse(match.document.data)
    printf "%<rank>i: #%<docid>3.3i %<title>s\n",
           rank: match.rank + 1,
           docid: match.docid,
           title: fields['TITLE']
    matches << match.docid
  end
  spy.values.each do |facet|
    printf "Facet: %<term>s; count: %<count>i\n",
           term: facet.term,
           count: facet.termfreq
  end

  # Finally, make sure we log the query and displayed results
  log_matches(querystring, offset, pagesize, matches)
### End of example code.
end

abort "Usage #{__FILE__} DBPATH QUERY..." if ARGV.length < 2

search(ARGV[0], ARGV[1..].join(' '))
