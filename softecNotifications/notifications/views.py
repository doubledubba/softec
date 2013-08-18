from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, csrf
from django.http import HttpResponse, Http404

from notifications.models import Computer, Restaurant, Agent, Owner
from notifications.helpers import digest, strToInt


@login_required
def listings(request):
    return render(request, 'notifications/listings.html')


@csrf.csrf_exempt
def check_in(request):
    if 'cid' not in request.POST or 'digest' not in request.POST:
        raise Http404
    cid = strToInt(request.POST['cid'])
    if digest(cid) != request.POST['digest']:
        return HttpResponse('Invalid digest', content_type='plain/text')
    computer = get_object_or_404(Computer, cid=cid)
    response = computer.check_in()
    return HttpResponse(response, content_type='plain/text')
