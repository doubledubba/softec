from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import logout


def index(request):
    return render(request, 'index.html')
    
def logout_user(request):
    logout(request)
    return redirect('/')
    
def login_user(request):
    '''pending implementation'''
    pass

