# -*- coding: utf-8 -*-

"""
.. note::

    对于 tags 这类有多个标签的情况, 如果用 KEYWORD 类型, 那么要求搜索的时候要完全匹配.
    而如果想要用全文搜索中的部分字幕匹配. 可以用逗号将其连接起来, 然后用 TEXT 类型索引.
"""

from __future__ import unicode_literals
import settings
import attr
from attrs_mate import AttrsClass
from whoosh import fields, qparser
from learn_whoosh.whoosh_index import get_index


@attr.s
class Movie(AttrsClass):
    genres = attr.ib()


class MovieSchema(fields.SchemaClass):
    genres = fields.KEYWORD(stored=True, commas=True, lowercase=True)


movie_schema = MovieSchema()
index = get_index(movie_schema, reset=True)

movie_data = [
    Movie(genres="Action,Biography,Crime,Drama"),
]

writer = index.writer()
for movie in movie_data:
    writer.add_document(**movie.to_dict())
writer.commit()

with index.searcher() as searcher:
    q = "crime"
    query = qparser.MultifieldParser(
        ["genres", ],
        schema=movie_schema
    ).parse(q)
    result = searcher.search(query)
    for doc in result:
        print(doc)
