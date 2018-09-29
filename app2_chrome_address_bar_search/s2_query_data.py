# -*- coding: utf-8 -*-

import settings
from learn_whoosh.browswer_bookmark.whoosh_index import get_index
from learn_whoosh.browswer_bookmark.whoosh_schema import bookmark_schema
from whoosh import qparser

idx = get_index(reset=False)
with idx.searcher() as searcher:
    q = "lear git engine"
    query = qparser.MultifieldParser(
        ["url", "title"],
        schema=bookmark_schema
    ).parse(q)
    result = searcher.search(query)
    for doc in result:
        print(doc)
