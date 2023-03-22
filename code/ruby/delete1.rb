#!/usr/bin/env ruby

require 'xapian'

def delete_docs(dbpath, identifiers)
  db = Xapian::WritableDatabase.new(dbpath, Xapian::DB_OPEN)
  identifiers.each do |identifier|
    idterm = "Q" + identifier
    db.delete_document idterm
  end
end

if ARGV.length < 2
  abort "Usage #{__FILE__} DBPATH ID..."
end

delete_docs ARGV[0], ARGV[1..]
