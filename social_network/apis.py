from datetime import datetime

from django.db.models import Count
from django.utils.datastructures import MultiValueDictKeyError
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password
from django.http import Http404
from django.db import transaction

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import status, viewsets
from rest_framework.views import APIView

from .models import User, Post, Like
from .serializers import UserSerializer, PostSerializer, LikeSerializer


class UserPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 50


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    pagination_class = UserPagination


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]


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
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        user = self.get_object(pk)
        request.data['password'] = make_password(request.data['password'])
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
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
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
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
    try:
        date_from = datetime.strptime(request.query_params['date_from'], "%Y-%m-%d")
        date_to = datetime.strptime(request.query_params['date_to'], "%Y-%m-%d")
    except MultiValueDictKeyError:
        return Response({
            "status": "error",
            "message": f"missing keys 'date_from' and/or 'date_to'"
        }, status=status.HTTP_400_BAD_REQUEST)
    except ValueError:
        return Response({
            "status": "error",
            "message": f"invalid date value"
        }, status=status.HTTP_400_BAD_REQUEST)

    #  likes for each day in a given date range
    likes = Like.objects.filter(publish_date__range=[date_from, date_to])\
        .extra(select={'day': 'date(logtime)'}).values('publish_date')\
        .order_by('-publish_date').annotate(likes=Count('id'))

    return Response(likes, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def smash_like_button(request, pk):
    user = request.user
    try:
        post = Post.objects.get(id=pk)
    except ObjectDoesNotExist:
        return Response({
            "status": "error",
            "message": f"Post with id={pk} does not exists.."
        }, status=status.HTTP_404_NOT_FOUND)

    with transaction.atomic():
        like = Like.objects.filter(user=user, post=post)
        if not like:
            Like.objects.create(user=user, post=post)
            post.likes = post.likes + 1
            post.save()
            return Response({"liked": True}, status=status.HTTP_201_CREATED)

        like.delete()
        post.likes = post.likes - 1
        post.save()
        return Response({"liked": False}, status=status.HTTP_201_CREATED)
