What data is there?
-------------------

Each row in the CSV file is an object from the catalogue, and has a number
of fields. There are:

id_NUMBER:
    a unique identifier
ITEM_NAME:
    a simple name, often from an established thesaurus
TITLE:
    a short caption
MAKER:
    the name of who made the object
DATE_MADE:
    when the object was made, which may be a range, approximate date or
    unknown
PLACE_MADE:
    where the object was made
MATERIALS:
    what the object is made of
MEASUREMENTS:
    the dimensions of the object
DESCRIPTION
    a description of the object
COLLECTION:
    the collection the object came from (eg: Science Museum - Space
    Technology)

There are obviously a number of different types of data here: free text,
identifiers, dates, places (which could be geocoded to geo coordinates),
and dimensions. Additionally, COLLECTION and MAKER both come from a list of
possible values.
