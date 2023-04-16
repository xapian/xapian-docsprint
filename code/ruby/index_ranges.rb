#!/usr/bin/env ruby
# frozen_string_literal: true

require 'xapian'
require 'json'
require_relative 'support'

def index(data_path, db_path)
  db = Xapian::WritableDatabase.new(db_path, Xapian::DB_CREATE_OR_OPEN)

  # Set up a TermGenerator that we'll use in indexing.
  term_generator = Xapian::TermGenerator.new
  term_generator.stemmer = Xapian::Stem.new('en')

  parse_csv_file(data_path).each do |row|
    doc = Xapian::Document.new
    term_generator.document = doc

    # Index each field with a suitable prefix.
    term_generator.index_text(row['TITLE'].to_s, 1, 'S')
    term_generator.index_text(row['DESCRIPTION'].to_s, 1, 'XD')

    # Index fields without prefixes for general search.
    term_generator.index_text(row['TITLE'].to_s)
    term_generator.increase_termpos
    term_generator.index_text(row['DESCRIPTION'].to_s)

    doc.data = row.to_h.to_json

### Start of example code.

    # parse the two values we need
    measurements = row['MEASUREMENTS'].to_s
    unless measurements.empty?
      numbers = numbers_from_string(measurements)
      doc.add_value(0, Xapian.sortable_serialise(numbers.max)) unless numbers.empty?

      date_made = row['DATE_MADE'].to_s
      years = numbers_from_string(date_made)
      doc.add_value(1, Xapian.sortable_serialise(years[0])) unless years.empty?
    end
### End of example code.

    # We use the identifier to ensure each object ends up in the
    # database only once no matter how many times we run the indexer.

    idterm = "Q#{row['id_NUMBER']}"
    doc.add_boolean_term(idterm)
    db.replace_document(idterm, doc)
  end
end

abort "Usage #{__FILE__} DATAPATH DBPATH" if ARGV.length < 2

index(ARGV[0], ARGV[1])
