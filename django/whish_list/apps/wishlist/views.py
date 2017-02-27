from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import User, Wish

def index(request):
    return render(request, ('wishlist/index.html'))

def register(request):
    if request.method == "POST":
        response = User.objects.register(request.POST)
        if response['status']:
            request.session['name'] = response['user'].first_name
            request.session['id'] = response['user'].id
            return redirect('wishlist:dashboard')
        else:
            errors = response['errors']
            for error in errors:
                messages.error(request, error)
            return redirect('wishlist:index')

def login (request):
    if request.method == "POST":
        response = User.objects.login(request.POST)
        if response['status']:
            request.session['name'] = response['user'].first_name
            request.session['id'] = response['user'].id
            return redirect('wishlist:dashboard')
        else:
            messages.error(request, response['errors'])
            return redirect('wishlist:index')

def dashboard(request):
    user = User.objects.get(id=request.session['id'])
    context = {
    "users" : User.objects.all(),
    "wishes" : Wish.objects.all(),
    "current": user
    }
    return render(request, ('wishlist/dashboard.html'), context)

def create(request):
    return render(request, ("wishlist/create.html"))

def new(request):
    user = request.session['id']
    response = Wish.objects.newWish(request.POST, user)
    if response:
        return redirect('wishlist:dashboard')
        messages.errors = response['errors']
    return redirect("wishlist:create")


def delete(request, wish_id):
    Wish.objects.delete(wish_id)
    return redirect("wishlist:dashboard")

def remove(request, wish_id):
    user_id = request.session['id']
    Wish.objects.remove(wish_user)
    return redirect("wishlist:dashboard")

def addto(request, wish_id):
    user_id = request.session['id']
    response = Wish.objects.addTo(wish_id, user_id)

    return redirect("wishlist:dashboard")
