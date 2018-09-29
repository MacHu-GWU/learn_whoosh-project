# -*- coding: utf-8 -*-

import attr
from attrs_mate import AttrsClass
from whoosh import fields


@attr.s
class Bookmark(AttrsClass):
    url = attr.ib()
    title = attr.ib()


class BookmarkSchema(fields.SchemaClass):
    url = fields.NGRAM(minsize=2, maxsize=10, stored=True)
    title = fields.NGRAM(minsize=2, maxsize=10, stored=True)


bookmark_schema = BookmarkSchema()
