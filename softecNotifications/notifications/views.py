from datetime import datetime
import json

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, Http404

from notifications.models import Computer, Restaurant, Agent, Owner
from notifications.helpers import digest, strToInt, logging
from softecNotifications.settings import CHECK_IN_RATE

logger = logging.getLogger(__name__)

@login_required
def listings(request):
    offline = [computer for computer in Computer.get_actives() if not
            computer.online]
    offline.sort(key=lambda x: x.restaurant.name)


    restaurants = [r.computer_set.all() for r in restaurants]

    params = {
        'offline_computers': offline,
        'restaurants': restaurants,
        'timestamp': datetime.now(),
    }
    return render(request, 'notifications/listings.html', params)


def dictize(obj, attrs):
    """Turns a python object into a dictionary"""
    model = {}
    for attr in attrs:
        if hasattr(obj, attr):
            value = getattr(obj, attr)
            if callable(value):
                value = value()
            model[attr] = value

    return model

from pprint import pformat
def listings_json(request):
    model = {'restaurants': []}
    restaurants = list(Restaurant.objects.filter(active=True)) # Find better solution
    restaurants.sort(key=lambda x: x.name.lower())
    for restaurant in restaurants:
        jRestaurant = {
            'name': restaurant.name,
            'url': restaurant.get_absolute_url(),
            'active': restaurant.active,
            'computers': [],
        }
        for computer in restaurant.computer_set.all():
            jComputer = dictize(computer, ['name', 'cid', 'is_active', 'online', 'notify_on_fail', 'js_warning', 'get_badge'])
            jRestaurant['computers'].append(jComputer)

        model['restaurants'].append(jRestaurant)

    data = json.dumps(model)

    return HttpResponse(data, content_type='text/plain')


@csrf_exempt
def update_view(request):
    cid = strToInt(request.POST['cid'])

    if 'cid' not in request.POST or 'digest' not in request.POST:
        logger.warning('Nice try hacker')
        raise Http404

    if digest(cid) != request.POST['digest']:
        data = (cid, request.POST['digest'])
        logger.warning('Auth failed for cid=%r, digest=%r' % data)
        return HttpResponse('Invalid digest', content_type='plain/text')


    try:
        computer = Computer.objects.get(cid=cid)
    except Computer.DoesNotExist:
        return HttpResponse('No existing computer with cid=%d' % cid, content_type='plain/text')
    computer.stamp_update()

    logging.info("Updated %d with CHECK_IN_RATE=%d" % (cid, CHECK_IN_RATE))
    return HttpResponse(CHECK_IN_RATE, content_type='plain/text')



@csrf_exempt
def check_in_view(request):
    if 'cid' not in request.POST or 'digest' not in request.POST:
        raise Http404
    cid = strToInt(request.POST['cid'])
    if digest(cid) != request.POST['digest']:
        return HttpResponse('Invalid digest', content_type='plain/text')
    computer = get_object_or_404(Computer, cid=cid)
    response = computer.check_in()
    logging.debug(response)
    return HttpResponse(response, content_type='plain/text')
#