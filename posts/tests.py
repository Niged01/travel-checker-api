'''tests for the travelled app'''
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Post


class PostListViewTests(APITestCase):
    '''testing list view for Posts'''
    def setUp(self):
        '''run before each test'''
        User.objects.create_user(username='nigel', password='pass')

    def test_can_list_Posts(self):
        '''test user can retrieve all Posts'''
        nigel = User.objects.get(username='nigel')
        Post.objects.create(owner=nigel, title='any title')
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_in_user_can_create_post(self):
        '''logged in user can create'''
        self.client.login(username='nigel', password='pass')
        response = self.client.post('/posts/', {'title': 'my title'})
        count = Post.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_logged_out_user_cant_create_post(self):
        '''test for logged out user unable to create achievement'''
        response = self.client.post('/posts/', {'title': 'my title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PostDetailViewTests(APITestCase):
    '''testing detail view for Posts'''
    def setUp(self):
        '''run before each test'''
        nigel = User.objects.create_user(username='nigel', password='pass')
        nick = User.objects.create_user(username='nick', password='pass')
        Post.objects.create(
            owner=nigel, title='my title', content='nigels  content'
        )
        Post.objects.create(
            owner=nick, title='his title', content='nicks content'
        )

    def test_can_retrieve_post_using_valid_id(self):
        '''test valid id shows post'''
        response = self.client.get('/posts/1/')
        self.assertEqual(response.data['title'], 'my title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_retrieve_post_using_invalid_id(self):
        '''test invalid id does not show post'''
        response = self.client.get('/posts/99/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_own_post(self):
        '''can owner update'''
        self.client.login(username='nigel', password='pass')
        response = self.client.put(
            '/posts/1/', {'title': 'a new title'}
        )
        post = Post.objects.filter(pk=1).first()
        self.assertEqual(post.title, 'a new title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_update_unowned_post(self):
        '''check user cant update someone elses post'''
        self.client.login(username='nigel', password='pass')
        response = self.client.put(
            '/posts/2/', {'title': 'a new title'}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
