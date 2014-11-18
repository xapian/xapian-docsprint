#!/usr/bin/env python

import xapian

### Start of class header and constructor.
class ExternalWeightPostingSource(xapian.PostingSource):
    """
    A Xapian posting source returning weights from an external source.
    """
    def __init__(self, wtsource):
        xapian.PostingSource.__init__(self)
        self.wtsource = wtsource
### End of class header and constructor.

### Start of init.
    def init(self, db):
        self.db = db
        self.alldocs = db.postlist('')
        self.set_maxweight(self.wtsource.get_maxweight())
### End of init.

### Start of termfreq methods.
    def get_termfreq_min(self): return self.db.get_doccount()
    def get_termfreq_est(self): return self.db.get_doccount()
    def get_termfreq_max(self): return self.db.get_doccount()
### End of termfreq methods.

### Start of get_weight.
    def get_weight(self):
        doc = self.db.get_document(self.current.docid)
        return self.wtsource.get_weight(doc)
### End of get_weight.

### Start of get_docid.
    def get_docid(self):
        return self.current.docid
### End of get_docid.

### Start of at_end.
    def at_end(self):
        return self.current is None
### End of at_end.

### Start of next.
    def next(self, minweight):
        try:
            self.current = self.alldocs.next()
        except StopIteration:
            self.current = None
### End of next.

### Start of skip_to.
    def skip_to(self, docid, minweight):
        try:
            self.current = self.alldocs.skip_to(docid)
        except StopIteration:
            self.current = None
### End of skip_to.
