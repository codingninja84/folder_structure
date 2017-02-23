from __future__ import unicode_literals
from django.db import models
import re, bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+.[a-zA-Z]+$')

class UserManager(models.Manager):
    def register(self, formData):
        #store possbile failed validations
        errors = []

        if len(formData['first_name']) < 2:
            errors.append("First name must be at least 2 characters long!")
        if len(formData['last_name']) < 2:
            errors.append("Last name must be at least 2 characters long!")
        if not len(formData['email']):
            errors.append("email is required")
        if not EMAIL_REGEX.match(formData['email']):
            errors.append("email is not valid")
        if len(formData['password']) < 8:
            errors.append("Password must be 8 char long!")
        if not formData['password'] == formData['confirm']:
            errors.append("Passwords must match")
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
            user = self.create(first_name=formData['first_name'], last_name=formData['last_name'], email=formData['email'], password=hashedPw)
            response['status'] = True
            response['user'] = user
            return response

    def login(self, form):
        response = {}
        user = User.objects.filter(email=form['email'])
        if user:
            if bcrypt.checkpw(form['password'].encode(), user[0].password.encode()):
                response['user'] = user[0]
                response['status'] = True
                return response
            else:
                response['status'] = False
                response['errors'] = "Invalid Password/Email Combo!"
                return response

class SecretManager(models.Manager):
    def newMsg(self, form, user_id):
        user = User.objects.get(id=user_id)
        print user.first_name
        thing = self.create(message=form['postsecret'], creator=user)
        return thing

    def like(self, user_id, message_id):
        message = Secret.objects.get(id=message_id)
        user = User.objects.get(id=user_id)
        message.liked_by.add(user)
        
class User(models.Model):
    first_name = models.CharField(max_length=38)
    last_name = models.CharField(max_length= 38)
    email = models.CharField(max_length= 25)
    password = models.CharField(max_length= 100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Secret(models.Model):
    message = models.CharField(max_length=1000)
    creator = models.ForeignKey(User, related_name="messages")
    liked_by = models.ManyToManyField(User, related_name="Likes")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = SecretManager()
