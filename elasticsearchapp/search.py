from elasticsearch.helpers import bulk
from elasticsearch_dsl import DocType, Text, Date
from elasticsearch_dsl.connections import connections

from . import models

es = connections.create_connection(
    hosts=['localhost'],
    http_auth=('elastic', 'changeme'),
    port=9200
)


class BlogPostIndex(DocType):
    author = Text()
    posted_date = Date()
    title = Text()
    text = Text()

    class Meta:
        index = 'blogpost-index'


def bulk_indexing():
    BlogPostIndex.init()
    bulk(client=es, actions=(b.indexing() for b in models.BlogPost.objects.all().iterator()))
