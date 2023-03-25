#!/usr/bin/env ruby

require 'xapian'
require 'json'
require_relative 'support'

def search(dbpath, querystring, materials, offset: 0, pagesize: 10)
  # offset - defines starting point within result set
  # pagesize - defines number of records to retrieve

  # Open the database we're going to search.
  db = Xapian::Database.new(dbpath)

### Start of example code.
  # Set up a QueryParser with a stemmer and suitable prefixes
  queryparser = Xapian::QueryParser.new
  queryparser.stemmer = Xapian::Stem.new("en")
  queryparser.stemming_strategy = Xapian::QueryParser::STEM_SOME
  queryparser.add_prefix("title", "S")
  queryparser.add_prefix("description", "XD")


  # And parse the query
  query = queryparser.parse_query(querystring)

  if materials.length > 0
    # Filter the results to ones which contain at least one of the
    # materials.

    # Build a query for each material value
    material_queries = materials.map { |material| 'XM' + material.downcase }

    # Build a query for each material value
    material_query = Xapian::Query.new(Xapian::Query::OP_OR, material_queries)

    # Use the material query to filter the main query
    query = Xapian::Query.new(Xapian::Query::OP_FILTER, query, material_query)
  end
### End of example code.

  # Use an Enquire object on the database to run the query
  enquire = Xapian::Enquire.new(db)
  enquire.query = query

  # And print out something about each match
  matches = []
  enquire.mset(offset, pagesize).matches.each do |match|
    fields = JSON.parse(match.document.data)
    printf "%i: #%3.3i %s\n", match.rank + 1, match.docid, fields['TITLE']
    matches << match.docid
  end
  log_matches(querystring, offset, pagesize, matches)
end
### End of example code.

if ARGV.length < 2
  abort "Usage #{__FILE__} DBPATH QUERY..."
end

search(ARGV[0], ARGV[1], ARGV[2..])
