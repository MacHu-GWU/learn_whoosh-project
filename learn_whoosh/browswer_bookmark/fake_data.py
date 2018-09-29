# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from .whoosh_schema import Bookmark

data = [
    Bookmark(url="https://github.com/MacHu-GWU/learn_whoosh-project",
             title="My Notes in learning whoosh, a great full text search engine in Python"),
]
data = [bm.to_dict() for bm in data]
