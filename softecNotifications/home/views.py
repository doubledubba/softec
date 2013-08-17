from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login


def index(request):
    return render(request, 'index.html', {'alert': 'success', 'message': 'fuck yeah', 'message_title': 'bitches'})
    
def logout_user(request):
    logout(request)
    return redirect('/')
    
def login_user(request):
    if request.method == 'GET':
        return render(request, 'sign_in.html')
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # Redirect to a success page.
            else:
                pass
                # Return a 'disabled account' error message
        else:
            pass
            # Return an 'invalid login' error message.
        return HttpResponse('post')
