# Given the cooperhewitt collection repo, find 100 objects and
# output a CSV.
#
# (c) James Aylett 2016
#
# The column names were chosen to be compatible with our existing
# code, which is based on a dataset constructed (a long time ago)
# from a Science Museum API...and so is idiosyncratic :-)
#
# The cooperhewitt dataset (https://github.com/cooperhewitt/collection/)
# was chosen because it is under CC0, and contains descriptions (which
# are helpful when demonstrating an IR system).

import csv
import json
import os
import os.path
import sys
import xapian

stopper = xapian.SimpleStopper('/usr/local/Cellar/xapian/1.4.3/share/xapian-core/stopwords/english.list')

with open('data/ch-objects.csv', 'w') as fh:
    w = csv.writer(fh, dialect='excel')
    w.writerow(
        [
            'id_NUMBER', # 0
            'NAME_unused',
            'TITLE', # 2
            'MAKER', # 3
            'DATE_MADE', # 4
            'PLACE_MADE_unused',
            'MATERIALS', # 6
            'MEASUREMENTS', # 7
            'DESCRIPTION', # 8
            'WHOLE_PART_unused',
            'COLLECTION', # 10
        ]
    )
    count = 0

    def walker():
        treegen = os.walk(os.path.join(sys.argv[1], 'objects'))
        for dir_entry in treegen:
            for fname in dir_entry[2]:
                if fname.endswith('.json'):
                    yield os.path.join(dir_entry[0], fname)

    for fname in walker():
        # We walk the tree, opening object files and filtering
        # to ones that are suitable. Suitable means they have
        # dimensions (which we convert to mm), 
        with open(fname, 'r') as fp:
            obj = json.load(fp)
        #print("Loaded '%s' from %s." % (obj.get('title_raw', 'Untitled'), fname))

        keys = set(obj.keys())
        # If we don't have the relevant keys, then skip this.
        REQUIRED_KEYS = {
            'accession_number', # should be a given
            'title_raw', # likewise
            'date',
            'dimensions_raw',
            'medium',
            'participants',
        }
        if not keys.issuperset(REQUIRED_KEYS):
            #print("Missing keys: %s" % (REQUIRED_KEYS - keys))
            continue

        def _pick(obj, *args):
            for arg in args:
                arg = obj.get(arg)
                if arg is not None and arg != '':
                    return arg.replace('\n', ' ')
            return ''

        # Too boring for us
        if _pick(obj, 'title_raw', 'title') in ('None', ''):
            continue

        def medium(s):
            medium_words = []
            for word in s.strip().lower().split():
                word = ''.join([ c for c in word if c.isalpha() ])
                if word != '' and not stopper(word):
                    medium_words.append(word)
            return ';'.join(medium_words)
        
        row = [
            obj['accession_number'],
            '', # backwards compatibility with previous dataset (internal name)
            _pick(obj, 'title_raw', 'title'),
            '', # makers will go here (3)
            _pick(obj, 'date'),
            '', # backwards compatibility with previous dataset (place made)
            medium(_pick(obj, 'medium')),
            '', # measurements will go here (7)
            _pick(obj, 'label_text', 'description'),
            '', # backwards compatibility with previous dataset (whole/part)
            '', # collection will go here (10)
        ]
        makers = []
        collection = 'Cooper Hewitt, Smithsonian Design Museum'
        for participant in obj['participants']:
            # This is a somewhat incomplete list of roles we
            # don't care about.
            if participant['role_name'] not in [
                    'Bequestor',
                    'Borrower',
                    'Buyer',
                    'Cataloguer',
                    'Agent',
                    'Featured Artist',
                    'Manufacturer',
                    'Collector',
                    'Dedicatee',
                    'Donor',
                    'Executor',
                    'Lender',
            ]:
                makers.append(participant)
            if participant['role_name'] == 'Lender':
                collection = participant['person_name']

        # We only want single-maker works
        if len(makers) != 1:
            #print("Wrong number of makers (%d)" % len(makers))
            continue
        row[3] = makers[0]['person_name']

        def _convert(dim):
            if dim[1] == 'centimeters':
                dim = float(dim[0]) * 10
                if float(int(dim)) == dim:
                    return int(dim)
                else:
                    return dim

        if obj['dimensions_raw'] is None:
            continue
        else:
            dims = set(obj['dimensions_raw'].keys())
            # This is a bit ugly, but basically ensures we treat dimensions
            # in the same order no matter what, and will ignore anything
            # that isn't either width+height or width+height+depth.
            if dims == {
                'width',
                'height'
            } or dims == {
                'width',
                'height',
                'depth'
            }:
                dimensions = [
                    _convert(d)
                    for d in
                    [
                        obj['dimensions_raw'][dim]
                        for dim in [ 'width', 'height', 'depth' ]
                        if dim in obj['dimensions_raw']
                    ]
                ]

                row[7] = (
                    ' x '.join([str(d) for d in dimensions]) + ' mm'
                )

        row[10] = collection
        w.writerow([c.encode('utf-8') for c in row])
        
        count += 1
        if count == 100:
            break
        
