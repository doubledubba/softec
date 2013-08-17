from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def listings(request):
    return render(request, 'notifications/listings.html')
