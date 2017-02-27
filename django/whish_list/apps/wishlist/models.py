from __future__ import unicode_literals
import re, bcrypt
from django.db import models

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+.[a-zA-Z]+$')

class UserManager(models.Manager):
    def register(self, formData):
        #store possbile failed validations
        errors = []

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

class WishManager(models.Manager):
    def newWish(self, formData, user_id):
        user = User.objects.get(id=user_id)
        response = {}
        if len(formData['wish_item']) > 3:
            wish = self.create(wish_name=formData['wish_item'])
            item = Wish.objects.get(id=wish.id)
            item.wisher.add(user)
            response['status'] = True
            return response
        else:
            response['status'] = False
            response['errors'] = "Must be longer than 3 char!!"
        return response
    def delete(self, wish_id):
        Wish.objects.get(id=wish_id).delete()
        return "Deleted"

    def remove(self, wish_id):
        Wish.objects.get(id=wish_id).delete()
        return "deleted"

    def addTo(self, wish_id, user_id):
        wish = Wish.objects.get(id=wish_id)
        user = User.objects.get(id=user_id)
        wish.wishes.add(user)
class User(models.Model):
    first_name = models.CharField(max_length=38)
    last_name = models.CharField(max_length= 38)
    email = models.CharField(max_length= 25)
    password = models.CharField(max_length= 100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Wish(models.Model):
    wish_name = models.CharField(max_length=40)
    wisher = models.ManyToManyField(User, related_name="wishers")
    wishes = models.ManyToManyField(User, related_name="wishes")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = WishManager()
