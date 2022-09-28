from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .serializer import BlogSerializer, LoginSerializer, PostSerializer, TagSerializer
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from api.models import Blog, Post, Tags
from rest_framework import generics
from api import serializer
# Create your views here.

class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        # import pdb
        # pdb.set_trace()
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class BlogAPIView(generics.ListCreateAPIView):
    serializer_class = BlogSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, APIView):
        blog = Blog.objects.all()

        """
         many=True means queryset contains a list of itmes and we need to serialize them
         and serialize.data will be a list
         """

        serializer = self.serializer_class(blog, many=True)  
        return Response(serializer.data)



@api_view(['GET', 'POST'])
def blogList(request):
    # import pdb
    # pdb.set_trace()
    if request.method == "GET":
        blog = Blog.objects.all()
        serializer = BlogSerializer(blog, many=True)
        obj = serializer.data
        # print(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        serializer = BlogSerializer
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def PostList(request):

    if request.method == "GET":
        blog = Post.objects.all()
        serializer = PostSerializer(blog, many=True)
        obj = serializer.data
        # print(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        serializer = PostSerializer
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def taglist(request):

    if request.method == "GET":
        blog = Tags.objects.all()
        serializer = TagSerializer(blog, many=True)
        obj = serializer.data
        # print(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        serializer = TagSerializer
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

