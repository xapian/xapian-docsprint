#!/usr/bin/env ruby

require 'xapian'
require 'json'
require_relative 'support'


def index_csv(data_path, db_path)
  # puts "#{data_path} #{db_path}"
  db = Xapian::WritableDatabase.new(db_path, Xapian::DB_CREATE_OR_OPEN)
  term_generator = Xapian::TermGenerator.new
  term_generator.stemmer = Xapian::Stem.new('en')
  parse_csv_file(data_path).each do |row|
    rec = row.to_h
    doc = Xapian::Document.new
    term_generator.document = doc
    term_generator.index_text row["TITLE"].to_s, 1, 'S'
    term_generator.index_text row["DESCRIPTION"].to_s, 1, 'XD'
    term_generator.index_text row["TITLE"].to_s
    term_generator.increase_termpos
    term_generator.index_text row["DESCRIPTION"].to_s
    doc.data = row.to_h.to_json
    idterm = "Q#{row["id_NUMBER"]}"
    doc.add_boolean_term idterm
    db.replace_document idterm, doc
  end
end

index_csv ARGV[0], ARGV[1]

