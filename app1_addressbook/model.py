##encoding=utf8

from __future__ import print_function, unicode_literals
from whoosh.index import create_in, open_dir
from whoosh.fields import *
from whoosh.qparser import *
import pandas as pd, numpy as np
import os, shutil

class Address(object):
    def __init__(self, street, city, state, zipcode, alias, memo, tags):
        self.street = street
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.alias = alias
        self.memo = memo
        self.tags = tags

def restart():
    path = "indexdir"
    try:
        os.mkdir(path)
    except:
        pass
    for fname in os.listdir(path):
        try:
            os.remove(os.path.join(path, fname))
        except:
            shutil.rmtree(os.path.join(path, fname))

def read_data():
    addressbook = pd.read_csv("addressbook.txt", sep="\t", dtype = {"zipcode": np.str}, encoding="utf8")
    
    for street, city, state, zipcode, alias, memo, tag1, tag2, tag3, tag4, tag5 in addressbook.values:
        tags = set()
        for tag in [tag1, tag2, tag3, tag4, tag5]:
            if type(tag) == unicode:
                tags.add(tag)
        tags = ",".join(tags)
        address = Address(street, city, state, zipcode, alias, memo, tags)
        yield address

def create_schema():
    schema = Schema(street=NGRAMWORDS(stored=True), 
                    city=NGRAM(stored=True),
                    state=TEXT(stored=True),
                    zipcode=NGRAM(stored=True),
                    alias=NGRAMWORDS(stored=True),
                    memo=NGRAMWORDS(stored=True),
                    tags=KEYWORD(commas=True, stored=True) )
    return schema

def write_index():
    restart()
    schema = create_schema()
    ix = create_in("indexdir", schema)
    writer = ix.writer()
    for address in read_data():
        writer.add_document(street=address.street,
                            city=address.city,
                            state=address.state,
                            zipcode=address.zipcode,
                            alias=address.alias,
                            memo=address.memo,
                            tags=address.tags,)
    writer.commit()
    
def test_query():
    ix = open_dir("indexdir")
    with ix.searcher() as searcher:
        qp = QueryParser("street", ix.schema)
        q = qp.parse("Center")
        for doc in searcher.search(q):
            print(doc)
            
restart()
write_index()
test_query()