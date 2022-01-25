from django.test import SimpleTestCase
from django.urls import resolve, reverse
from social_network import apis
from rest_framework_simplejwt import views as jwt_views


class TestUrls(SimpleTestCase):

    def test_get_token(self):
        url = reverse('get_token')
        self.assertEquals(resolve(url).func.view_class, jwt_views.TokenObtainPairView)

    def test_refresh_token(self):
        url = reverse('refresh_token')
        self.assertEquals(resolve(url).func.view_class, jwt_views.TokenRefreshView)

    def test_user_activity(self):
        url = reverse('user_activity', args=[10])
        self.assertEquals(resolve(url).func, apis.user_activity)

    def test_analytics(self):
        url = reverse('analytics')
        self.assertEquals(resolve(url).func, apis.analytics)

    def test_user_list(self):
        url = reverse('users')
        self.assertEquals(resolve(url).func.view_class, apis.UserList)

    def test_user_detail(self):
        url = reverse('user_detail', args=[7])
        self.assertEquals(resolve(url).func.view_class, apis.UserDetail)

    def test_post_list(self):
        url = reverse('posts')
        self.assertEquals(resolve(url).func.view_class, apis.PostList)

    def test_post_detail(self):
        url = reverse('post_detail', args=[12])
        self.assertEquals(resolve(url).func.view_class, apis.PostDetail)

    def test_smash_like_button(self):
        url = reverse('smash_like_button', args=[213])
        self.assertEquals(resolve(url).func, apis.smash_like_button)
