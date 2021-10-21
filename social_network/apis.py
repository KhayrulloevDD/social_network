from datetime import timedelta, datetime

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import status
from rest_framework.views import APIView

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password
from django.http import Http404

from .models import User, Post, Like
from .serializers import UserSerializer, PostSerializer
from social_network.services.decorators import last_request_time, last_request_time_fbv


class UserList(APIView):

    permission_classes = [IsAdminUser]

    @last_request_time
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    @last_request_time
    def post(self, request):
        request.data['password'] = make_password(request.data['password'])
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):

    permission_classes = [IsAdminUser]

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    @last_request_time
    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    @last_request_time
    def put(self, request, pk):
        user = self.get_object(pk)
        request.data['password'] = make_password(request.data['password'])
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @last_request_time
    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        return Response({
                    "status": "success",
                    "message": f"User with id={pk} has been deleted successfully!"
                }, status=status.HTTP_204_NO_CONTENT)


class PostList(APIView):

    permission_classes = [IsAuthenticated]

    @last_request_time
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    @last_request_time
    def post(self, request):
        request.data['owner'] = request.user.id
        post_serializer = PostSerializer(data=request.data)
        if post_serializer.is_valid():
            post_serializer.save()
            return Response(post_serializer.data, status=status.HTTP_201_CREATED)
        return Response(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetail(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    @last_request_time
    def get(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    @last_request_time
    def put(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @last_request_time
    def delete(self, request, pk):
        post = self.get_object(pk)
        post.delete()
        return Response({
                    "status": "success",
                    "message": f"Post with id={pk} has been deleted successfully!"
                }, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAdminUser])
@last_request_time_fbv
def user_activity(request, pk):
    try:
        user = User.objects.get(id=pk)
        return Response({
            "last_login": user.last_login,
            "last_request": user.last_request,
        }, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response({
            "status": "error",
            "message": f"User with id={pk} does not exists.."
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAdminUser])
@last_request_time_fbv
def analytics(request):
    date_from = datetime.strptime(request.data['date_from'], "%Y-%m-%d")
    date_to = datetime.strptime(request.data['date_to'], "%Y-%m-%d")
    delta = timedelta(days=1)
    response_data = {}
    while date_from <= date_to:
        likes_for_this_day = Like.objects.filter(publish_date=date_from).count()
        response_data[date_from.strftime("%Y-%m-%d")] = likes_for_this_day
        date_from += delta
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@last_request_time_fbv
def smash_like_button(request, pk):
    user = request.user
    post = Post.objects.get(id=pk)

    if Like.objects.filter(user=user, post=post):
        Like.objects.filter(user=user, post=post).delete()
        post.likes = post.likes - 1
        post.save()
        return Response({"liked": False}, status=status.HTTP_201_CREATED)

    Like.objects.create(user=user, post=post)
    post.likes = post.likes + 1
    post.save()
    return Response({"liked": True}, status=status.HTTP_201_CREATED)