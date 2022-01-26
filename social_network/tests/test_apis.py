import json

from django.urls import reverse
from django.test import Client
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.test import force_authenticate

from social_network.serializers import UserSerializer, PostSerializer, LikeSerializer
from social_network.models import User, Post, Like
from social_network.apis import UserList


class TestAPISetUp(APITestCase):
    def setUp(self):
        self.get_token_url = reverse("get_token")

        self.username = "admin"
        self.email = "admin@admin.com"
        self.password = "admin"

        self.admin_user = User.objects.create_superuser(username=self.username, email=self.email, password=self.password)

        self.token = self.client.post(self.get_token_url, {"username": self.username, "password": self.password})


class TestToken(TestAPISetUp):

    def setUp(self):
        super().setUp()

        self.user_data = {
            "username": self.username,
            "password": self.password
        }

    def test_get_token(self):
        response = self.client.post(self.get_token_url, self.user_data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)


class TestUsersAPI(TestAPISetUp):

    def setUp(self):
        super().setUp()
        self.users_url = reverse("users")
        self.user_detail_url = reverse("user_detail", args=[2])

        self.valid_user_data = {
            "username": "user1",
            "password": "user1"
        }

        self.invalid_user_data = {
            "username": "",
            "password": ""
        }

    def test_post_valid_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token.data['access'])
        response = self.client.post(self.users_url, data=json.dumps(self.valid_user_data),
                                    content_type='application/json')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_post_invalid_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token.data['access'])
        response = self.client.post(self.users_url, data=json.dumps(self.invalid_user_data),
                                    content_type='application/json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_user(self):
        self.test_post_valid_user()
        response = self.client.put(self.user_detail_url, data=json.dumps({
            "username": "user2",
            "password": "user2"
        }), content_type='application/json')

        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_get_user(self):
        self.test_post_valid_user()
        response = self.client.get(self.user_detail_url, content_type='application/json')

        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_get_un_existed_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token.data['access'])
        response = self.client.get(self.user_detail_url, content_type='application/json')
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_user(self):
        self.test_post_valid_user()
        response = self.client.delete(self.user_detail_url, content_type='application/json')

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)


class TestPostsAPI(TestAPISetUp):

    def setUp(self):
        super().setUp()
        self.posts = reverse("posts")
        self.post_detail = reverse("post_detail", args=[1])

        self.username = "user1"
        self.email = "user1@user1.com"
        self.password = "user1"

        self.admin_user = User.objects.create_user(username=self.username, email=self.email, password=self.password)

        self.token = self.client.post(self.get_token_url, {"username": self.username, "password": self.password})

        self.valid_post_data = {
            "title": "user1",
            "content": "user1"
        }

        self.invalid_user_data = {
            "title": "",
            "content": ""
        }

    def test_post_method_for_valid_post_data(self):
        pass

    def test_post_method_for_invalid_post_data(self):
        pass

    def test_put_post(self):
        pass

    def test_get_post(self):
        pass

    def test_get_un_existed_post(self):
        pass

    def test_delete_post(self):
        pass

# self.user_activity = reverse("user_activity", args=[22])
# self.analytics = reverse("analytics")
# self.smash_like_button = reverse("smash_like_button", args=[22])

