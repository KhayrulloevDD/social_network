from django.urls import path
from social_network import apis
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('get_token', jwt_views.TokenObtainPairView.as_view(), name='get_token'),
    path('refresh_token', jwt_views.TokenRefreshView.as_view(), name='refresh_token'),
    path('user_activity/<int:pk>', apis.user_activity, name='user_activity'),
    path('analytics', apis.analytics, name='analytics'),
    path('users', apis.UserList.as_view(), name='users'),
    path('users/<int:pk>', apis.UserDetail.as_view(), name='user_detail'),
    path('posts', apis.PostList.as_view(), name='posts'),
    path('posts/<int:pk>', apis.PostDetail.as_view(), name='post_detail'),
    path('smash_like_button/<int:pk>', apis.smash_like_button, name='smash_like_button'),
]
