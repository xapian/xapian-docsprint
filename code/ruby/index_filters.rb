#!/usr/bin/env ruby

require 'xapian'
require 'json'
require_relative 'support'


### Start of example code.
### Start of example code.
def index(data_path, db_path)
  # puts "#{data_path} #{db_path}"
  db = Xapian::WritableDatabase.new(db_path, Xapian::DB_CREATE_OR_OPEN)
  term_generator = Xapian::TermGenerator.new
  term_generator.stemmer = Xapian::Stem.new('en')
  parse_csv_file(data_path).each do |row|
    rec = row.to_h
    doc = Xapian::Document.new
    term_generator.document = doc
    term_generator.index_text(row["TITLE"].to_s, 1, 'S')
    term_generator.index_text(row["DESCRIPTION"].to_s, 1, 'XD')
    term_generator.index_text(row["TITLE"].to_s)
    term_generator.increase_termpos
    term_generator.index_text(row["DESCRIPTION"].to_s)

    ### Start of new indexing code.
    # Index the MATERIALS field, splitting on semicolons.
    row["MATERIALS"].to_s.split(';').each do |material|
      material.strip!
      material.downcase!
      if material.length > 0
        doc.add_boolean_term('XM' + material)
      end
    end
    ### End of new indexing code.

    doc.data = row.to_h.to_json
    idterm = "Q#{row["id_NUMBER"]}"
    doc.add_boolean_term(idterm)
    db.replace_document(idterm, doc)
  end
end
### End of example code.

if ARGV.length < 2
  abort "Usage #{__FILE__} DATAPATH DBPATH"
end

index(ARGV[0], ARGV[1])
