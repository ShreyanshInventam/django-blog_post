from dataclasses import field
from re import S
from unittest.util import _MAX_LENGTH
from rest_framework import  serializers
from api.models import User, Blog, Post, Tags
from django.contrib.auth import authenticate
from rest_framework.fields import CurrentUserDefault


class LoginSerializer(serializers.Serializer):
    """
    login through the username and password and returning the 
    API response with jwt token
    """
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)


    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        return {
            'email': user.email,
            'username': user.username,
            'token': user.token
        }


class BlogSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    title = serializers.CharField(max_length=255)
    slug = serializers.CharField()
    content = serializers.CharField()
    tags = serializers.PrimaryKeyRelatedField(queryset=Tags.objects.all(), required=False,
                                            many=True, write_only=False)
    category = serializers.CharField()

    class Meta:
        model = Blog
        fields = ['user', 'title', 'content', 'tags', 'category','slug',]

    
    def create(self, validated_data):
        tag = validated_data.pop('tags')
        obj= Blog.objects.create(**validated_data)
        if tag:
            obj.tags.set(tag)
        return obj


class PostSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    category = serializers.CharField()
    tags = serializers.PrimaryKeyRelatedField(queryset=Tags.objects.all(), required=False,
                                            many=True, write_only=False)
   
    # class Meta:
    #     model = Post
    #     fields = ['user', 'tags', 'category',]

    def create(self, validated_data):
        tag = validated_data.pop('tags')
        obj= Post.objects.create(**validated_data)
        if tag:
            obj.tags.set(tag)
        return obj


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tags
        fields = ['tags']
