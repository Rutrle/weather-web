from django.db import models
from django.contrib import auth

# Create your models here.


class User(auth.models.User, auth.models.PermissionsMixin):
    def __str__(self):
        return "@{}".format(self.username)

''' 
class UserPreference():
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    degrees = models.Choices()

    def __str__(self):
        return self.user.username + '_preferences'
'''