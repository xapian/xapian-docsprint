===================
Perl Specific Notes
===================

Unicode
#######

The Unicode support in Perl is good and straightforward as long as you
understand how it works. A string can be either a byte string
(encoded) or a character string (decoded). The correct way to deal
with this matter is to decode the strings on input and encode them on
output, while the code should deal with characters (not bytes, so a
character with diacritics is seen a single character, not 2 or more
bytes).

Typically, this is done this way::

  #!/usr/bin/env perl
  use utf8; # this says that in this file we can use unicode and will be decoded
  use strict;
  use warnings;
  # this encodes on output
  binmode STDOUT, ":encoding(UTF-8)";
  binmode STDERR, ":encoding(UTF-8)";

  # this opens a file and decodes it.
  open (my $in, '<:encoding(UTF-8)', $file);
  while (<$in>) { .... }

  # this opens a file for writing and encodes the output on print
  open (my $out, '>:encoding(UTF-8)', $file);
  print $out "Đe ši Šu\n";

Also, database drivers usually have a (recommended) setting to decode
the strings coming out from the DB and encoding them before storing
them, so the code deals transparently with characters.

How this applies to Xapian? You usually store strings with
``set_data`` and ``add_value``. Such fields are binary fields, so they
want bytes. If you pass a decoded string, it will be silently encoded.
When you are going to retrieve them, the data will come out encoded,
as a string of bytes, and you need to be prepared for it. You can do
this using serialization. The example code stores the documents data
using ``encode_json`` (which produces a byte string) and on retrieving
it calls ``decode_json`` (which returns decoded values). When you
store a value, you encode it with ``encode`` or with the
``sortable_serialise``. Both functions produce bytes::

  use Encode qw/encode decode/;
  use JSON::MaybeXS;
  # ....
  $doc->set_data(encode_json($rec));
  $doc->add_value(0, encode('UTF-8', $string));
  $doc->add_value(1, Search::Xapian::sortable_serialise($value));

If you retrieve a stored value, you need to decode it::

  use Encode qw/encode decode/;
  use JSON::MaybeXS;
  # ...
  my $string = decode('UTF-8', $doc->get_value(0));
  my $fields = decode_json($doc->get_data);

See :xapian-code-example:`index_facets` and
:xapian-code-example:`search_facets` for some example code.



