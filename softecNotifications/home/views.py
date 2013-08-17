from urllib import urlencode

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login

GetifyUrl = lambda url, mapping: url + '?' + urlencode(mapping)

def index(request):
    params = {
        'alert': request.GET.get('alert'),
        'message_title': request.GET.get('message_title'),
        'message': request.GET.get('message'),
    }
    return render(request, 'index.html', params)
    
def logout_user(request):
    logout(request)
    mapping = {'alert': 'info',
        'message_title': 'Bye bye!',
        'message': 'You have succesfully logged out!'
    }
    url = GetifyUrl('/', mapping)
    return redirect(url)
    
def login_user(request):
    if request.method == 'GET':
        next = {'next': request.GET.get('next') or '/'}
        login_url = GetifyUrl('/login/', next)
        return render(request, 'sign_in.html', {'login_url': login_url})
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                mapping = {'alert': 'success', 
                    'message_title': 'Success!', 
                    'message': 'You have successfully logged in!'
                }
                # Redirect to a success page.
            else:
                mapping = {'alert': 'danger',
                    'message_title': 'Uh oh!',
                    'message': 'Your account has been disabled!'
                }
                # Return a 'disabled account' error message
        else:
            mapping = {'alert': 'danger',
                'message_title': 'Woops!',
                'message': 'Your login information is incorrect. Try again!'
            }
            # Return an 'invalid login' error message.
        next = request.GET.get('next') or '/'
        if not next:
            next = '/'
        username = request.GET.get('username')
        if username:
            mapping['username'] = username
        url = GetifyUrl(next, mapping)
        return redirect(url)
