from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import User, Appointment
import datetime

def index(request):
    return render(request, ('appointment/index.html'))

def success(request):
    now =  datetime.date.today()
    context = {
    'now' : datetime.date.today(),
    'current': User.objects.get(id=request.session['id']),
    'appt': Appointment.objects.all(),
    'today' : Appointment.objects.filter(date=now),
    }
    return render(request, ('appointment/appointments.html'), context)

def createNew(request):
    user_id = request.session['id']
    response = Appointment.objects.createNew(request.POST, user_id)
    if response['status']:
        return redirect("users:success")
    else:
        errors = response['errors']
        for error in errors:
            messages.error(request, error)
        return redirect("users:success")
def editPage(request, apt_id):
    context = {
    'apt' : Appointment.objects.get(id=apt_id)
    }
    return render(request, ("appointment/edit.html"), context)

def edit(request, apt_id):
    Appointment.objects.edit(apt_id, request.POST)
    return redirect("users:success")

def register(request):
    if request.method == "POST":
        response = User.objects.register(request.POST)
        if response['status']:
            request.session['name'] = response['user'].first_name
            request.session['id'] = response['user'].id
            return redirect('users:success')
        else:
            errors = response['errors']
            for error in errors:
                messages.error(request, error)
            return redirect('users:index')

def login(request):
    if request.method == "POST":
        response = User.objects.login(request.POST)
        if response['status']:
            request.session['name'] = response['user'].first_name
            request.session['id'] = response['user'].id
            return redirect('users:succss')
        else:
            errors = response['errors']
            for error in errors:
                messages.error(request, error)
            return redirect('users:index')

def delete(request, apt_id):
    Appointment.objects.deleteApt(apt_id)
    return redirect('users:success')
def logout(request):
    request.session.clear()
    return redirect("users:index")
