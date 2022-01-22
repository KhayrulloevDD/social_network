from datetime import datetime

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import status
from rest_framework.views import APIView

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password
from django.http import Http404

from .models import User, Post, Like
from .serializers import UserSerializer, PostSerializer, LikeSerializer


class UserList(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

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

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk):
        user = self.get_object(pk)
        request.data['password'] = make_password(request.data['password'])
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        return Response({
                    "status": "success",
                    "message": f"User with id={pk} has been deleted successfully!"
                }, status=status.HTTP_204_NO_CONTENT)


class PostList(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

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

    def get(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = self.get_object(pk)
        post.delete()
        return Response({
                    "status": "success",
                    "message": f"Post with id={pk} has been deleted successfully!"
                }, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAdminUser])
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
def analytics(request):
    date_from = datetime.strptime(request.data['date_from'], "%Y-%m-%d")
    date_to = datetime.strptime(request.data['date_to'], "%Y-%m-%d")
    like_objects = Like.objects.filter(publish_date__range=[date_from, date_to])
    serializer = LikeSerializer(like_objects, many=True)

    # create dictionary of days for response with initial 0 values
    response_data = {}
    for item in serializer.data:
        response_data[item['publish_date']] = 0

    # count likes for each day
    for response_data_item in response_data:
        for serializer_data_item in serializer.data:
            if response_data_item == serializer_data_item['publish_date']:
                print(serializer_data_item['publish_date'])
                response_data[response_data_item] += 1

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
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
