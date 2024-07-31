from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

from decimal import Decimal


class Account(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    creation_date = models.DateField(auto_now_add=True)
    active = models.BooleanField(default=True)
    def __str__(self):
            return self.name

class CustomUser(AbstractUser):
    accounts = models.ManyToManyField(Account, blank=True, related_name='users')
    profile = models.OneToOneField('Profile', on_delete=models.CASCADE, null=True, blank=True, related_name='user')

    @property
    def profile_about(self):
        return self.profile.about

    def plant_tree(self, tree, location, account):
        from Trees.models import PlantedTree
        PlantedTree.objects.create(
            age=0,  # Assuming age is 0 when just planted
            tree=tree, # The tree seed will be chosen from the form
            user=self,
            account=account, # The chosen account will be the one used to plant 
            latitude=location[0],
            longitude=location[1]
        )

    def plant_trees(self, will_be_planted_trees, account):
        # The param: will_be_planted_trees countain all the trees instance and your locations
        from Trees.models import PlantedTree
        for tree, latitude, longitude in will_be_planted_trees:
            PlantedTree.objects.create(
                age=0,
                tree=tree, # The tree comes from the list param: will_be_planted_trees
                user=self,
                account=account,
                latitude=latitude, # The latitude comes from the list param: will_be_planted_trees
                longitude=longitude # The longitude comes from the list param: will_be_planted_trees
            )
    
class Profile(models.Model):
    about = models.TextField(null=True, blank=True)

    @property
    def user(self):
        return self.user.username
    
    def date_joined(self):
        return self.user.date_joined

    def __str__(self):
        return f'Profile of {self.user.username}'


