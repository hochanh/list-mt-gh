from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect

def persona_login(request):
    if request.method == 'POST':
        user = authenticate(assertion=request.POST['assertion'])
        if user:
            login(request, user)
        return HttpResponse('OK')
    else:
        return HttpResponse(status=404)

def persona_logout(request):
    logout(request)
    return redirect('/')
