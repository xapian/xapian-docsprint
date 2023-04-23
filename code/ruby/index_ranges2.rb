#!/usr/bin/env ruby
# frozen_string_literal: true

require 'xapian'
require 'json'
require_relative 'support'

def index(data_path, db_path)
  # Create or open the database we're going to be writing to.
  db = Xapian::WritableDatabase.new(db_path, Xapian::DB_CREATE_OR_OPEN)

  # Set up a TermGenerator that we'll use in indexing.
  term_generator = Xapian::TermGenerator.new
  term_generator.stemmer = Xapian::Stem.new('en')

  parse_states(data_path).each do |row|
    # We make a document and tell the term generator to use this.
    doc = Xapian::Document.new
    term_generator.document = doc

### Start of example code.
    # Index each field with a suitable prefix.
    term_generator.index_text(row['name'].to_s, 1, 'S')
    term_generator.index_text(row['description'].to_s, 1, 'XD')
    term_generator.index_text(row['motto'].to_s, 1, 'XM')

    # Index fields without prefixes for general search.
    term_generator.index_text(row['name'].to_s)
    term_generator.increase_termpos
    term_generator.index_text(row['description'].to_s)
    term_generator.increase_termpos
    term_generator.index_text(row['motto'].to_s)

    admitted = row['admitted'].to_s
    # Add document values.
    unless admitted.empty?
      doc.add_value(1, Xapian.sortable_serialise(admitted[0..3].to_i))
      doc.add_value(2, admitted) # YYYYMMDD
    end

    doc.add_value(3, Xapian.sortable_serialise(row['population'].to_i)) if row['population']

### End of example code.

    doc.data = row.to_h.to_json

    # We use the identifier to ensure each object ends up in the
    # database only once no matter how many times we run the indexer.

    idterm = "Q#{row['id_NUMBER']}"
    doc.add_boolean_term(idterm)
    db.replace_document(idterm, doc)
  end
end

abort "Usage #{__FILE__} DATAPATH DBPATH" if ARGV.length < 2

index(ARGV[0], ARGV[1])
