from elasticsearch.helpers import bulk
from elasticsearch_dsl import DocType, Text, Date, Search, Object
from elasticsearch_dsl.connections import connections

from .models import Blog, BlogPost, BlogPage

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

    @classmethod
    def trigger_delete(cls, instance):
        """
        Delete the index from Elastic Search
        :param instance: Object to be deleted
        """
        es.delete(instance.blog.index_name(), 'blog_post_index', instance.id)


class BlogPageIndex(DocType):
    title = Text()
    text = Text()
    blog = Text()

    @classmethod
    def trigger_delete(cls, instance):
        """
        Delete the index from Elastic Search
        :param instance: Object to be deleted
        """
        es.delete(instance.blog.index_name(), 'blog_page_index', instance.id)


def bulk_indexing():
    # NOTE Index name comes from the object 'Meta' itself
    bulk(client=es, actions=[
        post.indexing() for post in BlogPost.objects.all().iterator()
    ])
    bulk(client=es, actions=[
        page.indexing() for page in BlogPage.objects.all().iterator()
    ])


def _print_results(result):
    for hit in result.hits:
        print hit.blog, hit.meta.doc_type, hit.title


def _search(search_client, search_term):
    search_client = search_client.query('match', text=search_term)
    return search_client.execute()


def _search_blog(subdomain, search_term):
    blog = Blog.objects.get(subdomain=subdomain)
    s = Search(index=blog.index_name())
    return _search(s, search_term)


def search(text):
    """
    Searches inside all the indices
    :param text: Search Term
    :return: Hits
    """
    s = Search()
    result = _search(s, text)
    _print_results(result)
    return result


def search_umbra(text):
    """
    Searches inside the index for umbra3d
    :param text: Search Term
    :return: Hits
    """
    result = _search_blog('umbra3d', text)
    _print_results(result)
    return result


def search_postman(text):
    """
    Searches inside the index for postman
    :param text: Search Term
    :return: Hits
    """
    result = _search_blog('postman', text)
    _print_results(result)
    return result
