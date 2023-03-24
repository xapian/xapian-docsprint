#!/usr/bin/env ruby

require 'xapian'

### Start of example code.
def delete_docs(dbpath, identifiers)
  db = Xapian::WritableDatabase.new(dbpath, Xapian::DB_OPEN)
  identifiers.each do |identifier|
    idterm = "Q" + identifier
    db.delete_document(idterm)
  end
end
### End of example code.

if ARGV.length < 2
  abort "Usage #{__FILE__} DBPATH ID..."
end

delete_docs(ARGV[0], ARGV[1..])
