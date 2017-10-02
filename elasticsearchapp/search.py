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
    for blog in Blog.objects.all():
        index_name = 'blogpost-index-{}'.format(blog.subdomain)
        # Create Index and map BlogPostIndex to it
        BlogPostIndex.init(index=index_name, using=es)
        # Index Posts
        # NOTE Need to provide index name while bulk indexing
        bulk(client=es, actions=(
            post.indexing() for post in BlogPost.objects.filter(blog=blog).iterator()
        ))


def _print_results(result):
    for hit in result.hits:
        print hit.blog, hit.title


def _search_blog(subdomain, search_term):
    blog = Blog.objects.get(subdomain=subdomain)
    s = Search().query('match', blog=blog.subdomain).filter('term', text=search_term)
    return s.execute()


def search(text):
    s = Search().filter('term', text=text)
    result = s.execute()
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
