from django.shortcuts import render

def listings(request):
    return render(request, 'notifications/listings.html')
