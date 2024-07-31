from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from ..models import *
from Users.models import Account

class UserTreeListViewTestCase(TestCase):
    def setUp(self):
        # Create Accounts
        self.account1 = Account.objects.create(name='Account 1')
        self.account2 = Account.objects.create(name='Account 2')

        # Create Plants
        self.plant1 = Plant.objects.create(name='Plant 1', scientific_name='test1')
        self.plant2 = Plant.objects.create(name='Plant 2', scientific_name='test2')

        # Create Users
        self.user1 = get_user_model().objects.create_user(username='user1', password='password', email='user1@example.com')
        self.user2 = get_user_model().objects.create_user(username='user2', password='password', email='user2@example.com')
        self.user3 = get_user_model().objects.create_user(username='user3', password='password', email='user3@example.com')

        #Assign users to accounts
        self.user1.accounts.add(self.account1, self.account2)
        self.user2.accounts.add(self.account1, self.account2)
        self.user3.accounts.add(self.account1, self.account2)

        # Plant trees
        PlantedTree.objects.create(tree=self.plant1, user=self.user1, account=self.account1, latitude='10.000000', longitude='20.000000')
        PlantedTree.objects.create(tree=self.plant2, user=self.user1, account=self.account1, latitude='10.000000', longitude='20.000000')
        PlantedTree.objects.create(tree=self.plant1, user=self.user2, account=self.account1, latitude='11.000000', longitude='21.000000')
        PlantedTree.objects.create(tree=self.plant2, user=self.user3, account=self.account2, latitude='12.000000', longitude='22.000000')

        # Login
        self.client.login(username='user1', password='password')

    def test_user_tree_list_view(self):
        # Acess template
        url = reverse('trees:garden', kwargs={'user_id': self.user1.id, 'account_id': self.account1.id})
        response = self.client.get(url)

        # Test response
        self.assertEqual(response.status_code, 200)

        # Test get plants
        self.assertContains(response, 'Plant 1')
        self.assertContains(response, 'Plant 2')
        self.assertNotContains(response, 'Plant 3')

    def test_access_other_user_trees(self):
        #Login in other user
        self.client.login(username='user2', password='password')

        # Get plant
        planted_tree = PlantedTree.objects.filter(user=self.user1, account=self.account1).first()

        # Acess template
        url = reverse('trees:tree_detail', kwargs={'pk': planted_tree.id, 'user_id': self.user1.id, 'account_id': self.account1.id})
        response = self.client.get(url)

        # Test Response
        self.assertEqual(response.status_code, 403)

    def test_list_all_trees_account(self):
        # Acess template
        url = reverse('trees:account_garden', kwargs={'account_id': self.account1.id})
        response = self.client.get(url)
        
        # Test Response
        self.assertEqual(response.status_code, 200)

        # Test get plants
        self.assertContains(response, 'Plant 1')
        self.assertContains(response, 'Plant 2')
        self.assertNotContains(response, 'Plant 3')
