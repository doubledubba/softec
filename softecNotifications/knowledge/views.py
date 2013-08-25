from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext

from knowledge.models import Article
from knowledge.choices import base_categories as categories

from search import search, simpleSearch

import time


def index(request):
    params = {}
    articles = None
    get = lambda param: request.GET[param] if param in request.GET else None

    params['content'] = get('content')
    params['title'] = get('title')
    params['description'] = get('description')
    params['keywords'] = get('keywords')

    params['category'] = get('categories')

    q = get('q')
    sq = get('sq')

    searched = False # prevents search from happening twice
    # if q and sq: only q results

    startTime = datetime.now()

    if (q or params['category']) and not searched:
        articles = search(q, params)
        searched = True
        params['q'] = q

    if sq and not searched:
        articles = simpleSearch(sq)
        searched = True
        params['sq'] = sq

    params['latency'] = (datetime.now() - startTime).total_seconds()

    params['passed_query'] = searched and (sq or q) and articles
    params['query'] = q or sq

    if not articles:
        articles = Article.objects.all() 
        params['failed_query'] = True

    if not articles: # could still be empty list after db query --> None
        redirect('/thanks/computers_no')

    params['articles'] = articles

# params need
# content title description keywords category
# latency query failed_query articles

    return render_to_response('knowledge/index.html', params,
            context_instance=RequestContext(request))
        

def update_hit(article):
    if article.views:
        article.views += 1
    else:
        article.views = 1

    article.save()


def show_article(request, pk):

    if not pk.isdigit():
        try:
            article = get_object_or_404(Article, title=str(pk))
        except Article.MultipleObjectsReturned:
            msg = 'Multiple articles named "%s".' % pk
            msg += '\nUse primary key hyperlinks instead'
            return render_to_response('thanks.html', {'msg': msg, 'alert_type':
                'error'}, context_instance=RequestContext(request))

    else:
        article = get_object_or_404(Article, pk=pk)

    update_hit(article)

    if request.user.is_authenticated():
        show = True
    else:
        show = article.public

    if not show:
        return redirect('/login/')

    params = {'article': article, 'show': show}

    return render_to_response('knowledge/article.html', params,
        context_instance=RequestContext(request))
    

def show_raw_article(request, pk):

    if not pk.isdigit():
        try:
            article = get_object_or_404(Article, title=pk)
        except Article.MultipleObjectsReturned:
            msg = 'Multiple articles named "%s".' % pk
            msg += '\nUse primary key hyperlinks instead'
            return render_to_response('thanks.html', {'msg': msg, 'alert_type':
                'error'}, context_instance=RequestContext(request))

    else:
        article = get_object_or_404(Article, pk=pk)

    update_hit(article)

    if request.user.is_authenticated():
        show = True
    else:
        show = article.public

    if not show:
        return redirect('/login/')

    params ={'article': article, 'raw': True, 'show': show}
    return render_to_response('knowledge/article.html', params,
        context_instance=RequestContext(request))

