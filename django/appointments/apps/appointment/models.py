from __future__ import unicode_literals
import re, bcrypt
from django.db import models
import datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+.[a-zA-Z]+$')

class UserManager(models.Manager):
    def register(self, formData):
        #store possbile failed validations
        errors = []
        dob = formData['dob']
        dateParts = dob.split("-")
        print dateParts
        if len(formData['first_name']) < 3:
            errors.append("First name must be at least 2 characters long!")
        if len(formData['last_name']) < 3:
            errors.append("Last name must be at least 2 characters long!")
        if not len(formData['email']):
            errors.append("email is required")
        if not EMAIL_REGEX.match(formData['email']):
            errors.append("email is not valid")
        if len(formData['password']) < 8:
            errors.append("Password must be 8 char long!")
        if not formData['password'] == formData['confirm']:
            errors.append("Passwords must match")
        if len(dateParts) < 3:
            errors.append("Not a valid birthday")
        user = User.objects.filter(email= formData['email'])

        if user:
            errors.append("Email must be unique!")

        response = {}

        if errors:
            response['status'] = False
            response['errors'] = errors
            return response
        else:
            hashedPw = bcrypt.hashpw(formData['password'].encode(), bcrypt.gensalt())
            user = self.create(first_name=formData['first_name'], last_name=formData['last_name'], email=formData['email'], password=hashedPw, dob=(formData['dob']))
            response['status'] = True
            response['user'] = user
            return response

    def login(self, formData):
        response = {}
        errors = []

        if not len(formData['email']):
            errors.append("email is required")
        if not EMAIL_REGEX.match(formData['email']):
            errors.append("email is not valid")
        if len(formData['password']) < 8:
            errors.append("Password must be 8 char long!")

        else:
            user = User.objects.filter(email=formData['email'])
            if user:
                if bcrypt.checkpw(formData['password'].encode(), user[0].password.encode()):
                    response['user'] = user[0]
                    response['status'] = True
                    return response
                else:
                    response['status'] = False
                    response['errors'] = "Invalid Password/Email Combo!"
                    return response
        response['status'] = False
        response['errors'] = errors
        return response

class AppointmentManager(models.Manager):
    def createNew(self, formData, user_id):
        response = {}
        errors = []
        if len(formData['tasks']) < 3:
            errors.append("Must be a task longer than 3 char!")
        if len(formData['date']) < 3:
            errors.append("Must be a task longer than 3 char!")
        if errors:
            response['errors'] = errors
            response['status'] = False
            return response
        else:
            dateParts = formData['date'].split("-")
            creator = User.objects.get(id=user_id)
            apt = self.create(tasks=formData['tasks'], user=creator, status="pending", date=formData['date'], time=formData['time'])
            task = Appointment.objects.get(id=apt.id)
            response['status'] = True
            return response

    def edit(self, apt_id, formData):
        Appointment.objects.filter(id=apt_id).update(tasks=formData['tasks'], status=formData['select'], date=formData['date'], time= formData['time'])

    def deleteApt(self, apt_id):
        Appointment.objects.get(id=apt_id).delete()


class User(models.Model):
    first_name = models.CharField(max_length=38)
    last_name = models.CharField(max_length= 38)
    email = models.CharField(max_length= 25)
    password = models.CharField(max_length= 100)
    dob = models.DateTimeField(auto_now_add=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Appointment(models.Model):
    tasks = models.CharField(max_length=40)
    user = models.ForeignKey(User, related_name="user_tasks")
    status = models.CharField(max_length=40)
    date = models.DateField(auto_now=False)
    time = models.TimeField(auto_now=False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = AppointmentManager()
