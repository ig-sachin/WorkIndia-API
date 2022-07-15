from itsdangerous import Serializer
from rest_framework import serializers
from .models import Questions
from django.contrib.auth.models import User


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


# Serializer for Register User
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'date_joined')
        extra_kwargs = {'password': {'write_only': True},
                        'date_joined': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'], validated_data['email'], validated_data['password'], date_joined=validated_data['date_joined'])

        return user


# Serializer for Question Model
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        fields = '__all__'
