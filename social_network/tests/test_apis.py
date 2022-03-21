import json
import pdb

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from social_network.models import User, Post


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
#
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
        self.post_url = reverse("posts")
        self.post_detail_url = reverse("post_detail", args=[1])

        self.username = "user1"
        self.email = "user1@user1.com"
        self.password = "user1"

        self.admin_user = User.objects.create_user(username=self.username, email=self.email, password=self.password)

        self.token = self.client.post(self.get_token_url, {"username": self.username, "password": self.password})

        self.valid_post_data = {
            "title": "title#1",
            "content": "content#1"
        }

        self.invalid_user_data = {
            "title": "",
            "content": ""
        }

    def test_post_method_for_valid_post_data(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token.data['access'])
        response = self.client.post(self.post_url, data=json.dumps(self.valid_post_data),
                                    content_type='application/json')

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_post_method_for_invalid_post_data(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token.data['access'])
        response = self.client.post(self.post_url, data=json.dumps(self.invalid_user_data),
                                    content_type='application/json')

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_post(self):
        self.test_post_method_for_valid_post_data()
        owner = User.objects.get(username=self.username)
        response = self.client.put(self.post_detail_url, data=json.dumps({
                "title": "updated title",
                "content": "updated content",
                "owner": owner.id,
            }), content_type='application/json')

        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_get_post(self):
        self.test_post_method_for_valid_post_data()
        response = self.client.get(self.post_detail_url, content_type='application/json')

        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_get_un_existed_post(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token.data['access'])
        response = self.client.get(self.post_detail_url, content_type='application/json')

        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_post(self):
        self.test_post_method_for_valid_post_data()
        response = self.client.delete(self.post_detail_url, content_type='application/json')

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)


class TestOtherFeatures(TestAPISetUp):
    def setUp(self):
        super().setUp()
        self.user_activity_url_existed_user = reverse("user_activity", args=[1])
        self.user_activity_url_not_existed_user = reverse("user_activity", args=[7])
        self.analytics_url = reverse("analytics")
        self.smash_like_button_url_existed_post = reverse("smash_like_button", args=[1])
        self.smash_like_button_url_not_existed_post = reverse("smash_like_button", args=[6])

    def test_user_activity_url_with_existed_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token.data['access'])
        response = self.client.get(self.user_activity_url_existed_user, content_type='application/json')

        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_user_activity_url_with_not_existed_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token.data['access'])
        response = self.client.get(self.user_activity_url_not_existed_user, content_type='application/json')

        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_analytics_url_with_valid_data(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token.data['access'])
        response = self.client.get(self.analytics_url, {
            "date_from": "2021-12-25",
            "date_to": "2022-01-31"
        })

        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_analytics_url_with_invalid_data(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token.data['access'])
        response = self.client.get(self.analytics_url, {
            "date_from": "",
        })

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_smash_like_button_url_existed_post(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token.data['access'])
        Post.objects.create(title="title#1", content="content#1", owner_id=1)
        response = self.client.post(self.smash_like_button_url_existed_post, content_type='application/json')

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_smash_like_button_url_not_existed_post(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token.data['access'])
        response = self.client.post(self.smash_like_button_url_not_existed_post, content_type='application/json')

        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)
