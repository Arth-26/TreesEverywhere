from django.db import models
from Users.models import Account, CustomUser
from decimal import Decimal

class Plant(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    scientific_name = models.CharField(max_length=255, null=True, blank=True)

    def count_planted_trees(self):
        return self.planted_tree.count()

    def __str__(self):
        return self.name

class PlantedTree(models.Model):
    age = models.IntegerField(default=0)
    planted_at = models.DateField(auto_now_add=True)
    tree = models.ForeignKey(Plant, on_delete=models.CASCADE, null=False, related_name='planted_tree')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, related_name='planted_trees')
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=False, related_name='planted_trees')
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    #Functions to customize the display of some model data
    def location(self):
        location = f'Lat: {self.latitude}, Long: {self.longitude}'
        return location
    
    def get_user(self):
        return self.user.username
    
    def get_account(self):
        return self.account.name
    
    def planted_tree(self):
        return self.tree.name
    
    def get_scientific_name(self):
        return self.tree.scientific_name


    def save(self, *args, **kwargs):
        # Formatting the decimal latitude and longitude fields to the standard world format
        self.latitude = Decimal(str(self.latitude).replace(',', '.'))
        self.longitude = Decimal(str(self.longitude).replace(',', '.'))
        super(PlantedTree, self).save(*args, **kwargs)

    def __str__(self):
        return f'Tree {self.tree.name} planted by {self.user.username}'
    