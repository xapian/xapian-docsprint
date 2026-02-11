=======================
Term Tokenisation Rules
=======================

The rules for turning a piece of text into terms when indexing and for turning
a query string into terms when searching are very similar.

Abbreviation/Acronyms/Initialisms
=================================

A sequence of two or more Unicode upper case letters each separated by `.` is
handled specially to better handle abbreviations, acronyms and initialisms.  So
`P.T.O` is handled the same as `PTO`.  A trailing `.` is allowed but not
required.

Infix Characters
================

Some punctuation characters may be present within a term (but not at the
start/end).  Each such infix character must have a "word character" before
and after it.  Most infix characters are included in the term, but a few
are skipped:

+-----------+---------------------------+-----------------+
| Codepoint | Description               | Notes           |
+-----------+---------------------------+-----------------+
| U+00AD    | SOFT HYPHEN               | Since 2.0.0     |
| U+200B    | ZERO WIDTH SPACE          | < 2.0.0 only    |
| U+200C    | ZERO WIDTH NON-JOINER     |                 |
| U+200D    | ZERO WIDTH JOINER         |                 |
| U+2060    | WORD JOINER               |                 |
| U+FEFF    | ZERO WIDTH NO-BREAK SPACE |                 |
+-----------+---------------------------+-----------------+

Infix Characters for Numbers
----------------------------

If both preceded and followed by a Unicode digit then the following
infix characters are allowed:

+-----------+------------------------------------------+------+
| Codepoint | Description                              | Char |
+-----------+------------------------------------------+------+
| U+002C    | COMMA                                    | `,`  |
| U+002E    | FULL STOP                                | `.`  |
| U+003B    | SEMICOLON                                | `:`  |
| U+037E    | GREEK QUESTION MARK                      | `;`  |
| U+0589    | ARMENIAN FULL STOP                       | `։`  |
| U+060D    | ARABIC DATE SEPARATOR                    | `؍`  |
| U+07F8    | NKO COMMA                                | `߸`  |
| U+2044    | FRACTION SLASH                           | `⁄`  |
| U+FE10    | PRESENTATION FORM FOR VERTICAL COMMA     | `︐` |
| U+FE13    | PRESENTATION FORM FOR VERTICAL COLON     | `︓` |
| U+FE14    | PRESENTATION FORM FOR VERTICAL SEMICOLON | `︔` |
+-----------+------------------------------------------+------+

Infix Characters for Words
--------------------------

Otherwise the following infix characters are allowed (this list is based
on the Unicode word boundary rules):

+-----------+------------------------------------------+------+-------------+
| Codepoint | Description                              | Char | Replacement |
+-----------+------------------------------------------+------+-------------+
| U+0026    | AMPERSAND                                | `&`  |             |
| U+0027    | APOSTROPHE                               | `'`  |             |
| U+00B7    | MIDDLE DOT                               | `·`  |             |
| U+2019    | RIGHT SINGLE QUOTATION MARK              | `’`  | `'`         |
| U+201B    | SINGLE HIGH-REVERSED-9 QUOTATION MARK    | `‛`  | `'`         |
| U+2027    | HYPHENATION POINT                        | `‧`  |             |
+-----------+------------------------------------------+------+-------------+

The various apostrophe characters (`'`, `U+2019` and `U+201B`) are all
normalised to `'`.

Suffix Characters
=================

Up to 3 suffix characters are allowed and included on the end of the word.
The current suffix characters are `+` and `#`.

Phrase Generators
=================

A group of terms each separated by one or more of the following punctuation
characters is handled as a phrase search: `.-/:\@`

So for example, `joe-blogs@example.org` becomes a phrase search for the terms
`joe`, `blogs`, `example` and `org`.
