'''Testing for the travelled list, list and detail'''
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Travelled


# taken from DRF_API walkthrough with modifications
class TravelledListViewTests(APITestCase):
    '''test the travelled list view'''
    def setUp(self):
        '''setup runs before every test method'''
        User.objects.create_user(username='nigel', password='pass')

    def test_can_list_travelled(self):
        '''check a user can list all the posts'''
        nigel = User.objects.get(username='nigel')
        Travelled.objects.create(owner=nigel, content='testing travelled')
        response = self.client.get('/travelled/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_in_user_can_create_travelled(self):
        '''test to see if logged in user can create a post'''
        self.client.login(username='nigel', password='pass')
        response = self.client.post('/travelled/', {'content': 'testing'})
        count = Travelled.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_not_logged_in_cannot_create_travelled(self):
        '''test for non logged in user unable to post memos'''
        response = self.client.post(
            '/travelled/', {'content': 'testing again'}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TravelledDetailViewTests(APITestCase):
    '''retrieving and updating travelled'''
    def setUp(self):
        '''set up runs before each test'''
        nigel = User.objects.create_user(username='nigel', password='pass')
        nick = User.objects.create_user(username='nick', password='pass')
        Travelled.objects.create(
            owner=nigel, content='nigels content'
        )
        Travelled.objects.create(
            owner=nick, content='nicks content'
        )

    def test_user_can_retrieve_travelled_using_valid_id(self):
        '''check travelled can be retrieved with valid id'''
        response = self.client.get('/travelled/1/')
        self.assertEqual(response.data['content'], 'nigels content')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cannot_retrieve_travelled_with_invalid_id(self):
        '''cannot get a travelled with invalid id'''
        response = self.client.get('/travelled/99/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_own_travelled(self):
        '''can an owner update their travelled'''
        self.client.login(username='nigel', password='pass')
        response = self.client.put(
            '/travelled/1/', {'content': 'new content'}
        )
        travelled = Travelled.objects.filter(pk=1).first()
        self.assertEqual(travelled.content, 'new content')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cannot_update_travelled_they_dont_own(self):
        '''check a user cant update someone elses travelled'''
        self.client.login(username='nigel', password='pass')
        response = self.client.put(
            '/travelled/2/', {'content': 'different text'}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)