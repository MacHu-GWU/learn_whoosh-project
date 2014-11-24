##encoding=utf8

"""
Field说明 = http://pythonhosted.org//Whoosh/api/fields.html

stored – Whether the value of this field is stored with the document.
unique – Whether the value of this field is unique per-document.
"""

from __future__ import print_function, unicode_literals
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import *
from whoosh.qparser.dateparse import DateParserPlugin
from datetime import datetime, date, timedelta
import os, shutil

def restart():
    path = "indexdir"
    for fname in os.listdir(path):
        try:
            os.remove(os.path.join(path, fname))
        except:
            shutil.rmtree(os.path.join(path, fname))
restart()

def example00():
    """
    这是官方文档中的例子，展示了whoosh中的几个基本抽象概念
    """
    ## 定义document schema。本例中文档有3个属性，title是TEXT类型，path是ID类型，content是TEXT类型
    ## 类型的概念以及参数stored的意义在后面的例子中均有介绍
    schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT)
    ## 定义index(简写ix)。按照我们定义的schema，全文搜索引擎就会为不同的字段自动添加index
    ## index有writer，和searcher两大子类
    ix = create_in("indexdir", schema)
    
    ## 创建writer类，将数据通过writer写入index。writer和数据库一样，也有commit这个机制
    writer = ix.writer()
    writer.add_document(title="First document", path="/a",
                        content="This is the first document we've added!")
    writer.add_document(title="Second document", path="/b",
                        content="The second one is even more interesting!")
    writer.commit()
    
    ## 创建搜索器
    with ix.searcher() as searcher:
        ## 创建QueryParser类，这个类是用来将用户输入的搜索串解析成服务器能理解query
        queryparser = QueryParser("content", ix.schema)
        ## 通过.parse方法创建query
        query = queryparser.parse("first")
        ## 将query传入sercher进行搜索
        results = searcher.search(query)
        print(results[0])
    
example00()

def example01():
    """whoosh.fields.ID
    ID类似于数据库中primary key的概念，根据primary key进行SELECT的时候必须ID完全匹配上，对大小写敏感。
    所以ID适合用来储存文档中具有唯一标志符的属性，例如：
        document_path
        document_url
        create_time_stamp    
    """
    schema = Schema(filepath=ID(stored=True))
    ix = create_in("indexdir", schema)
    
    writer = ix.writer()
    writer.add_document(filepath = "C:\python27\scripts")
    writer.commit()

    with ix.searcher() as searcher:
        query = QueryParser("filepath", ix.schema).parse("C:\python27\scripts")
        print(searcher.search(query)[0])
        query = QueryParser("filepath", ix.schema).parse("C:\Python27\scripts")
        print(searcher.search(query)[0])
        
# example01()

def example02():
    """whoosh.fields.IDLIST
    IDLIST类似数据库中多个primary key的概念，同样对大小写敏感。其他部分请参考ID篇
    """
    schema = Schema(city_and_state=IDLIST(stored=True), )
    ix = create_in("indexdir", schema)
    
    writer = ix.writer()
    writer.add_document(city_and_state = "arlington VA")
    writer.commit()

    with ix.searcher() as searcher:
        query = QueryParser("city_and_state", ix.schema).parse("arlington", "VA")
        print(searcher.search(query)[0])
        query = QueryParser("city_and_state", ix.schema).parse("VA, arlington")
        print(searcher.search(query)[0])
        query = QueryParser("city_and_state", ix.schema).parse("arlington")
        print(searcher.search(query)[0])
        query = QueryParser("city_and_state", ix.schema).parse("VA")
        print(searcher.search(query)[0])
        
# example02()

def example03():
    """whoosh.fields.STORED
    STORED表示无法被搜索到，但是每次其他单元被搜索到，都会自动跟着被显示
    """
    schema = Schema(SSN=ID(stored=True), memo=STORED, )
    ix = create_in("indexdir", schema)
    
    writer = ix.writer()
    writer.add_document(SSN = "123456", memo = "he is my best friend in high school")
    writer.commit()

    with ix.searcher() as searcher:
        query = QueryParser("SSN", ix.schema).parse("123456")
        print(searcher.search(query)[0])
        query = QueryParser("memo", ix.schema).parse("he is my best friend in high school") # unsearchable
        print(searcher.search(query)[0])
        
# example03()

def example04():
    """whoosh.fields.KEYWORD
    KEYWORD适合用于标签类的对象。每一个document拥有若干个标签，这若干标签可以相同。和IDLIST不同的是，
    可能很多个文档共同享有同一个标签集合。
    """
    schema = Schema(tags=KEYWORD(stored=True, commas=True))
    ix = create_in("indexdir", schema)
    
    writer = ix.writer()
    writer.add_document(tags = "action,romance,story,war")
    writer.commit()

    with ix.searcher() as searcher:
        query = QueryParser("tags", ix.schema).parse("story", "war")
        print(searcher.search(query)[0])
        query = QueryParser("tags", ix.schema).parse("war action")
        print(searcher.search(query)[0])
        
# example04()

def example05():
    """whoosh.fields.TEXT
    TEXT适用于文本对象，搜索方式类似于短语搜索，搜索的最小单位是词，对大小写不敏感。例如：
    "am", "boy" ===> "I am a boy"
    TEXT的主要对象是词，对数字和词的混合搜索支持不良好。
    如果要支持任意字母片段的匹配，请参考ngram算法部分
    """
    schema = Schema(sentence=TEXT(stored=True))
    ix = create_in("indexdir", schema)
    
    writer = ix.writer()
    writer.add_document(sentence = "I live in 1400 S Joyce St")
    writer.commit()

    with ix.searcher() as searcher:
#         query = QueryParser("sentence", ix.schema).parse("live", "joyce")
#         print(searcher.search(query)[0])
#         query = QueryParser("sentence", ix.schema).parse("joyce", "1400")
#         print(searcher.search(query)[0])
#         query = QueryParser("sentence", ix.schema).parse("live", "1400", "joyce") # 数字单词混合，无法匹配
#         print(searcher.search(query)[0])
#         query = QueryParser("sentence", ix.schema).parse("joy") # 单词片段，无法匹配
#         print(searcher.search(query)[0])
        
        qp = QueryParser("sentence", ix.schema)
        qp.add_plugin(WildcardPlugin()) # 字符模糊搜索扩展
        q = qp.parse("S joy*")
        print(searcher.search(q)[0])
        
# example05()

def example06():
    """whoosh.fields.NUMERIC
    数值型对象，有int, float两类
    """
    schema = Schema(temperature=NUMERIC(float, stored=True))
    ix = create_in("indexdir", schema)
    
    writer = ix.writer()
    writer.add_document(temperature = 32.3)
    writer.commit()

    with ix.searcher() as searcher:
        qp = QueryParser("temperature", ix.schema)
        qp.add_plugin(GtLtPlugin()) # 大于小于 支持扩展
        q = qp.parse("temperature:>=20.0")
        print(searcher.search(q)[0])

        qp.add_plugin(OperatorsPlugin(And="&")) # 与或非 支持扩展
        q = qp.parse("temperature:>=20.0 & temperature:<=40.0")
        print(searcher.search(q)[0])
        
        qp.add_plugin(RangePlugin()) # 范围区间 支持扩展
        q = qp.parse("temperature:{20 to]")
        print(searcher.search(q)[0])
        
# example06()

def example07():
    """whoosh.fields.DATETIME
    """
    schema = Schema(create_date=DATETIME(stored=True))
    ix = create_in("indexdir", schema)
    
    writer = ix.writer()
    writer.add_document(create_date = datetime(2014,1,10,6,30,0))
    writer.commit()

    with ix.searcher() as searcher:
        qp = QueryParser("create_date", ix.schema)
        qp.add_plugin(DateParserPlugin()) # DateParserPlugin自带了大于，小于区间等语法
        q = qp.parse("2014-01-10-06-30-00")
        print(searcher.search(q)[0])
        
        q = qp.parse("create_date:[20140110063000 to ]") # whoosh支持最良好的就是年月日小时分钟秒连续写在一起的格式
        print(searcher.search(q)[0])
        
        qp.add_plugin(OperatorsPlugin())
        q = qp.parse("create_date:[201403 to] OR [to 201402] ")
        print(searcher.search(q)[0])
        
# example07()

def example08():
    """whoosh.fields.NGRAM
    NGRAM将整个文本拆分成词，然后把每个词拆分成小块。
    """
    schema = Schema(tweets=NGRAM(minsize=2, maxsize=6, stored=True))
    ix = create_in("indexdir", schema)
    
    writer = ix.writer()
    writer.add_document(tweets="Heard that? Kate just get a boyfriend!")
    writer.commit()
    
    with ix.searcher() as searcher:
        qp = QueryParser("tweets", schema)
        q = qp.parse("oyfrien") # 成功，因为在
        print(searcher.search(q)[0])
        q = qp.parse("boyfriend") # 成功，匹配整个词
        print(searcher.search(q)[0])
        q = qp.parse("e ju") # 不成功，因为空格跨越了词
        print(searcher.search(q)[0])

# example08()

def example09():
    """whoosh.fields.NGRAMWORDS
    NGRAMWORDS将整个文本拆分成字母块，无视词语，包括空格标点符号在内都拆分成小块
    """
    schema = Schema(tweets=NGRAMWORDS(minsize=2, maxsize=8, stored=True))
    ix = create_in("indexdir", schema)
    
    writer = ix.writer()
    writer.add_document(tweets="Heard that? Kate just get a boyfriend!")
    writer.commit()
    
    with ix.searcher() as searcher:
        qp = QueryParser("tweets", schema)
        q = qp.parse("oyfrien") # 成功，因为在
        print(searcher.search(q)[0])
        q = qp.parse("boyfriend") # 成功，匹配整个词
        print(searcher.search(q)[0])
        q = qp.parse("e ju") # 成功，因为是拆分的整个文本
        print(searcher.search(q)[0])

# example09()

def example10():
    """根据多个字段进行全文搜索
    """
    schema = Schema(name=TEXT(stored=True), height=NUMERIC(float, stored=True))
    ix = create_in("indexdir", schema)
    
    writer = ix.writer()
    writer.add_document(name = "Jack", height=180.5)
    writer.commit()
    
    with ix.searcher() as searcher:
        qp = QueryParser(None, schema)
        qp.add_plugin(MultifieldPlugin(["name", "height"]) ) # 多字段搜索parser 
        qp.add_plugin(GtLtPlugin())
        q = qp.parse("Jack height:>=180.5")
        print(searcher.search(q)[0])

# example10()






