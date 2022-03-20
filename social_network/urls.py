from django.urls import path
from social_network import apis

urlpatterns = [
    path('user_activity/<int:pk>', apis.user_activity, name='user_activity'),
    path('analytics', apis.analytics, name='analytics'),
    path('users', apis.UserList.as_view(), name='users'),
    path('users/<int:pk>', apis.UserDetail.as_view(), name='user_detail'),
    path('posts', apis.PostList.as_view(), name='posts'),
    path('posts/<int:pk>', apis.PostDetail.as_view(), name='post_detail'),
    path('smash_like_button/<int:pk>', apis.smash_like_button, name='smash_like_button'),
]
