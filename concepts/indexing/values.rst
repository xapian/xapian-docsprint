Values
======

`Values` are in a sense a more flexible version of terms. Each document can
have a set of values associated with it, which hold pieces of data which
can be useful during a search. These pieces of data could be things such as
keys which you want to be able to sort the results on, numeric values used
for range searches, or numbers to be used to affect the weight calculated
for documents during the search.

Each value is stored in a numbered `slot`; so for example, a document might
have a value indicating a category in slot 0, a value indicating a price in
slot 1, and a value indicating some measure of the importance of the
document in slot 10.  It's fine to use widely separated slot numbers - the
data isn't stored in a simple array.  Slot numbers can be any 32 bit
unsigned integer, except for ``0xffffffff`` which has a special meaning
(it's :xapian-constant:`BAD_VALUENO` which is used to indicate things like "not
sorting on any value slot").

The core of Xapian treats the contents of value slots as opaque binary
strings, rather than having support for numeric value types.  This becomes
significant if you want to perform range searches based on a value stored in
a slot, or to sort results based on the value stored in a slot.  To allow
this type of use of slots, Xapian provides a utility function,
`sortable_serialise`, which serialises a numeric value into a binary string
in such a way that the sort order of the resulting binary string matches
the numeric sort order of the unserialised values.

It is important to keep the amount of data stored in the values to a
minimum, since the values for a large number of documents may be read
during the search, and unused information will thus slow the search down.
Developers are sometimes tempted to use the value slots to hold information
which should really be stored in the document's data area; don't succumb to
this temptation!
