# -*- coding: utf-8 -*-

import settings
from learn_whoosh.browswer_bookmark.whoosh_index import get_index
from learn_whoosh.browswer_bookmark.fake_data import data

idx = get_index(reset=True)
writer = idx.writer()
for bookmark_data in data:
    writer.add_document(**bookmark_data)
writer.commit()
