from elasticsearch.helpers import bulk
from elasticsearch_dsl import DocType, Text, Date, Search, Object
from elasticsearch_dsl.connections import connections

from .models import Blog, BlogPost

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
    blog = Text()
    metadata = Object()


def bulk_indexing():
    # NOTE Index name comes from the object 'Meta' itself
    bulk(client=es, actions=[
        post.indexing() for post in BlogPost.objects.all().iterator()
    ])


def _print_results(result):
    for hit in result.hits:
        print hit.blog, hit.title


def _search(search_client, search_term):
    search_client = search_client.query('match', text=search_term)
    return search_client.execute()


def _search_blog(subdomain, search_term):
    blog = Blog.objects.get(subdomain=subdomain)
    index_name = 'blogpost-index-{}'.format(blog.subdomain)
    s = Search(index=index_name)
    return _search(s, search_term)


def search(text):
    s = Search()
    result = _search(s, text)
    _print_results(result)
    return result


def search_umbra(text):
    result = _search_blog('umbra3d', text)
    _print_results(result)
    return result


def search_postman(text):
    result = _search_blog('postman', text)
    _print_results(result)
    return result
