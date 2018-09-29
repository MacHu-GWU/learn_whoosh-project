Leverage power Full Text search for your App in Pure Python
==============================================================================
Full text is so powerful, and does these magic (and more):

1. Apple Address Book: contact search.
2. iTune: music search.
3. Google Chrome Address Bar: url search.
4. Forum site: post search.
...

`whoosh <https://pypi.python.org/pypi/whoosh>`_ is a pure python implemented full text search engine. It's light, and fast.

Let's learn!


Important Concepts in ``whoosh``:

- index, `whoosh.index.Index`:
- schema, `whoosh.fields.SchemaClass`: document schema definition, collection of field definition.
- field, `whoosh.fields.FieldType` and its children: defines how each field can be searched.
- query, `whoosh.fields.qparser`: parse string, and construct query
- results, `whoosh.searching.Results`: collection of matched document
- hit, `whoosh.searching.Hit`: a document match