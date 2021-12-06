from rest_framework import serializers
from .models import User, Post, Like


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'likes', 'owner', 'publish_date']


class UserSerializer(serializers.ModelSerializer):

    # posts = PostSerializer(many=True, source='post_set')

    class Meta:
        model = User
        fields = '__all__'
        # fields = ['id', 'username']


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ['publish_date']
        # depth = 1
