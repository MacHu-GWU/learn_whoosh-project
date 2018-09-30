# -*- coding: utf-8 -*-

"""
.. note::

    NGRAM 是将字符换成


"""

from __future__ import unicode_literals
import settings
import attr
from attrs_mate import AttrsClass
from whoosh import fields, qparser
from learn_whoosh.whoosh_index import get_index


@attr.s
class Bookmark(AttrsClass):
    url = attr.ib()
    title = attr.ib()


class BookmarkSchema(fields.SchemaClass):
    url = fields.NGRAM(minsize=2, maxsize=10, stored=True)
    title = fields.NGRAM(minsize=2, maxsize=10, stored=True)


bookmark_schema = BookmarkSchema()
index = get_index(bookmark_schema, reset=True)

# insert some test data
bookmark_data = [
    Bookmark(url="https://github.com/MacHu-GWU/learn_whoosh-project",
             title="My Notes in learning whoosh, a great full text search engine in Python"),
    Bookmark(url="https://github.com/MacHu-GWU/learn_git-project",
             title="Git 是最好的 版本控制工具"),
]

writer = index.writer()
for bookmark in bookmark_data:
    writer.add_document(**bookmark.to_dict())
writer.commit()

# run query
index = get_index(bookmark_schema, reset=False)
with index.searcher() as searcher:
    q = "工具"
    query = qparser.MultifieldParser(
        ["url", "title"],
        schema=bookmark_schema
    ).parse(q)
    result = searcher.search(query)
    for doc in result:
        print(doc)
