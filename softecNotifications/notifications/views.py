from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, Http404

from notifications.models import Computer, Restaurant, Agent, Owner
from notifications.helpers import digest, strToInt
from softecNotifications.settings import CHECK_IN_RATE, logging

logger = logging.getLogger(__name__)


@login_required
def listings(request):
    return render(request, 'notifications/listings.html')


@csrf_exempt
def update(request):

    if 'cid' not in request.POST or 'digest' not in request.POST:
        raise Http404

    cid = strToInt(request.POST['cid'])

    if digest(cid) != request.POST['digest']:
        #raise Http404
        return HttpResponse('Invalid digest', content_type='plain/text')


    computer = get_object_or_404(Computer, cid=cid)
    computer.last_update = datetime.now()
    computer.save()

    logging.info("Updated %d with CHECK_IN_RATE=%d" % (cid, CHECK_IN_RATE))
    return HttpResponse(CHECK_IN_RATE, content_type='plain/text')



@csrf_exempt
def check_in(request):
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