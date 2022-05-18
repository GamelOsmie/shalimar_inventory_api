from rest_framework import serializers
from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class UserCreateSerializer(UserCreateSerializer):

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'role', 'first_name', 'middle_name', 'last_name', 'workplace', 'is_verified', 'is_active')


class UserDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'slug', 'email', 'role', 'first_name', 'middle_name', 'last_name', 'workplace', 'is_verified', 'is_active')
