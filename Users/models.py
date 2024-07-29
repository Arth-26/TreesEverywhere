from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class Account(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    creation_date = models.DateField(auto_now_add=True)
    active = models.BooleanField(default=True)
    def __str__(self):
            return self.name

class CustomUser(AbstractUser):
    accounts = models.ManyToManyField(Account, related_name='users')
    profile = models.OneToOneField('Profile', on_delete=models.CASCADE, null=True, blank=True, related_name='user')

    @property
    def profile_joined(self):
        return self.date_joined
    
class Profile(models.Model):
    about = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'Profile of {self.user.username}'


