from django.urls import path, include
from social_network import apis
from rest_framework.routers import DefaultRouter


# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'users', apis.UserViewSet, basename="users")
router.register(r'posts', apis.PostViewSet, basename="posts")


urlpatterns = [
    path('user_activity/<int:pk>', apis.user_activity, name='user_activity'),
    path('analytics', apis.analytics, name='analytics'),
    path('', include(router.urls)),
    path('smash_like_button/<int:pk>', apis.smash_like_button, name='smash_like_button'),
]
