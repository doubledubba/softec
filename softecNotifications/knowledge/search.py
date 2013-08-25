from knowledge.models import Article

import time

field_queries = [
        'title__istartswith',
        'title__iendswith',
        'description__icontains',
        'keywords__icontains',
        'title__icontains'
        ]


def simpleSearch(query):
    '''Takes a user query string and yields a list of possible results.

    Searches over each word in the string and returns the cumulative results,
    using pre-built database queries that are not influenced by the user.'''

    query = query.split()
    articles = []

    for q in query:
        for field in field_queries:
            results = Article.objects.filter(**{field: q})
            if not results: continue
            for article in results:
                if article.pk not in articles:
                    articles.append(article.pk)
                    yield article




def search(query, params):
    '''Takes a user query string dictionary of GET parameters to yield an
    iterable of search results.'''

    articles = Article.objects.filter()
    category = params['category']
    del params['category']

    if category:
        articles == articles.filter(category=category)

    return articles


    


