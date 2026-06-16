from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['email','username','password']
        extra_kwargs={'password':{'write_only':True}}
    def create(self, validated_data):
        user=User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user
class LoginSerializer(serializers.Serializer):
    email=serializers.EmailField()
    password=serializers.CharField(write_only=True)
    def validate(self,attrs):
        attrs=attrs['email']
        password=password['password']
        