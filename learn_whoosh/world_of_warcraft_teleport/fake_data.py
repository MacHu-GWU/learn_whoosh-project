# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from .whoosh_schema import GPS

data = [
    GSP(x=0, y=0, z=0, map=0),
]
data = [bm.to_dict() for bm in data]
