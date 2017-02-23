from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import User, Secret
# Create your views here.
def index(request):
    return render(request, "dojo_secrets/index.html")

def register(request):
    response = User.objects.register(request.POST)
    if response['status']:
        request.session['name'] = response['user'].first_name
        request.session['id'] = response['user'].id
        request.session['user'] = repsonse['user']
        return redirect('secrets:secrets')
    else:
        errors = response['errors']
        for error in errors:
            messages.error(request, error)
        return redirect('secrets:index')
def login(request):
    if request.method == "POST":
        response = User.objects.login(request.POST)
        if response['status']:
            request.session['name'] = response['user'].first_name
            request.session['id'] = response['user'].id
            return redirect('secrets:secrets')
        else:
            messages.error(request, response['errors'])
            return redirect('secrets:index')
def logout(request):
    request.session.clear()
    return redirect('secrets:index')

def secrets(request):
    context = {
    "message": Secret.objects.all().order_by('-created_at')[:5],
    "user": User.objects.all()
    }
    if not request.session['name']:
        return redirect('secrets:index')
    return render(request, 'dojo_secrets/secrets.html', context)

def postsecret(request):
    Secret.objects.newMsg(request.POST, request.session['id'])

    return redirect('secrets:secrets')

def likes(request, message):
    message_id = message
    Secret.objects.like(request.session['id'], message_id)

    return redirect('secrets:secrets')

def popular(request):
    context = {
    "message": Secret.objects.all().order_by('-created_at')[:5],
    "user": User.objects.all()
    }
    return render(request, 'dojo_secrets/popular.html', context)
