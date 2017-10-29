#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
在微信里输入几个字就能找到联系人，在Chrome浏览器的地址栏里，输入几个字就能在历史记录和
收藏夹里找到链接。这个背后的关键技术叫做全文搜索。whoosh是一个纯Python实现的全文搜索引擎。
本例子就实现了一个简单的Chrome浏览器地址栏。
"""

from __future__ import unicode_literals
import attr
import time
import bs4
import multiprocessing
from pathlib_mate import Path
from whoosh import index, fields, qparser

index_dir = Path(__file__).change(new_basename="index")


def clear():
    """
    Remove index dir (reset everything).
    """
    import shutil
    try:
        shutil.rmtree(index_dir.abspath)
    except:
        pass


clear()


@attr.s
class Url(object):
    url = attr.ib()
    name = attr.ib()


class UrlSchema(fields.SchemaClass):
    url = fields.NGRAM(minsize=2, maxsize=10, stored=True)
    name = fields.NGRAM(minsize=2, maxsize=10, stored=True)


url_schema = UrlSchema()

if index_dir.exists():
    index_exists = True
    ix = index.open_dir(index_dir.abspath)
else:
    index_exists = False
    index_dir.mkdir()
    ix = index.create_in(
        Path(__file__).change(new_basename="index").abspath,
        url_schema,
    )


def insert_test_data():
    writer = ix.writer(procs=multiprocessing.cpu_count(), limitmb=128)

    # export your google bookmark somewhere
    p = "/Users/sanhehu/Documents/bookmarks_10_28_17.html"

    with open(p, "rb") as f:
        html = f.read().decode("utf-8")
    soup = bs4.BeautifulSoup(html, "lxml")

    url_set = set()
    data = list()
    for a in soup.find_all("a"):
        url = unicode(a.attrs["href"])
        name = unicode(a.text)
        if url not in url_set:
            url_set.add(url)
            data.append(Url(url=url, name=name))
    for url in data[:100]:
        writer.add_document(**attr.asdict(url))
    writer.commit()


if not index_exists:  # if not exists, insert data
    st = time.clock()
    insert_test_data()
    print("elapsed %.6f sec. " % (time.clock() - st,))

with ix.searcher() as s:
    q = "http" # put your query here
    query = qparser.MultifieldParser(["url", "name"], schema=url_schema).parse(
        q)
    res = s.search(query)
    for doc in res:
        print(doc)
