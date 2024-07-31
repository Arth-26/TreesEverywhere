from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import Account
from Trees.models import PlantedTree, Plant

class UserAndTreeTestCase(TestCase):

    def setUp(self):
        #Create Accounts
        self.account1 = Account.objects.create(name='Account 1')
        self.account2 = Account.objects.create(name='Account 2')

        #Create Users
        self.user1 = get_user_model().objects.create_user(username='user1', password='password', email='user1@example.com')
        self.user2 = get_user_model().objects.create_user(username='user2', password='password', email='user2@example.com')
        self.user3 = get_user_model().objects.create_user(username='user3', password='password', email='user3@example.com')

        #Assign users to accounts
        self.user1.accounts.add(self.account1, self.account2)
        self.user2.accounts.add(self.account1, self.account2)
        self.user3.accounts.add(self.account1, self.account2)

        self.client.login(username='user1', password='password')
        
    def test_plant_tree_function(self):
        #Create plant
        plant = Plant.objects.create(name='Alecrim', scientific_name='test_scientific_name1')

        # Call function 
        self.user1.plant_tree(plant, (15.000000, 25.000000), self.account1)

        # Test
        planted_tree = PlantedTree.objects.get(user=self.user1, account=self.account1)
        self.assertIsNotNone(planted_tree)

    def test_plant_trees_function(self):
        #Create plants
        plant1 = Plant.objects.create(name='Alecrim', scientific_name='test_scientific_name1')
        plant2 = Plant.objects.create(name='Coqueiro', scientific_name='test_scientific_name2')
        plant3 = Plant.objects.create(name='Macieira', scientific_name='test_scientific_name3')

        # Assigning parameters
        param_list = [(plant1, 15.000000, 25.000000),(plant2, 25.000000, 15.000000),(plant3, 10.000000, 20.000000)]

        # Call function
        self.user1.plant_trees(param_list, self.account1)

        #Test
        planted_tree = PlantedTree.objects.filter(user=self.user1, account=self.account1)
        self.assertIsNotNone(planted_tree)
        for tree in planted_tree:
            print(f'Tree name: {tree.tree.name}')

        
    