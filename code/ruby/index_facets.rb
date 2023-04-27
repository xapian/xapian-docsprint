#!/usr/bin/env ruby
# frozen_string_literal: true

require 'xapian'
require 'json'
require_relative 'support'

### Start of example code.
def index(data_path, db_path)
  db = Xapian::WritableDatabase.new(db_path, Xapian::DB_CREATE_OR_OPEN)

  # Set up a TermGenerator that we'll use in indexing.
  term_generator = Xapian::TermGenerator.new
  term_generator.stemmer = Xapian::Stem.new('en')

  parse_csv_file(data_path).each do |row|
    title = row['TITLE'].to_s
    description = row['DESCRIPTION'].to_s
    identifier = row['id_NUMBER'].to_s
    collection = row['COLLECTION'].to_s
    maker = row['MAKER'].to_s

    # We make a document and tell the term generator to use this.
    doc = Xapian::Document.new
    term_generator.document = doc

    # Index each field with a suitable prefix.
    term_generator.index_text(title, 1, 'S')
    term_generator.index_text(description, 1, 'XD')

    # Index fields without prefixes for general search.
    term_generator.index_text(title)
    term_generator.increase_termpos
    term_generator.index_text(description)

    # Add the collection as a value in slot 0.
    doc.add_value(0, collection)

    # Add the maker as a value in slot 1.
    doc.add_value(1, maker)

    # Store all the fields for display purposes.
    doc.data = row.to_h.to_json

    # We use the identifier to ensure each object ends up in the
    # database only once no matter how many times we run the indexer.
    idterm = "Q#{identifier}"
    doc.add_boolean_term(idterm)
    db.replace_document(idterm, doc)
  end
end
### End of example code.

abort "Usage #{__FILE__} DATAPATH DBPATH" if ARGV.length < 2

index(ARGV[0], ARGV[1])
