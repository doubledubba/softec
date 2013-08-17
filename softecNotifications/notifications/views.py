from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from notifications.models import Computer, Restaurant, Agent, Owner


@login_required
def listings(request):
    return render(request, 'notifications/listings.html')
