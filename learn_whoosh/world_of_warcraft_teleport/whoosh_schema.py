# -*- coding: utf-8 -*-

import attr
from attrs_mate import AttrsClass
from whoosh import fields


@attr.s
class GPS(AttrsClass):
    x = attr.ib()
    y = attr.ib()
    z = attr.ib()
    zone_id = attr.ib()

    expension = attr.ib()
    map = attr.ib()


class GPSSchema(fields.SchemaClass):
    url = fields.NGRAM(minsize=2, maxsize=10, stored=True)
    title = fields.NGRAM(minsize=2, maxsize=10, stored=True)
    tags = fields.KEYWORD()


gps_schema = GPSSchema()
