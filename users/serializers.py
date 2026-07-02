from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterSerializer(serializers.ModelSerializer):
    
    class Meta:
        
        model=User
        fields=[
            'email',
            'username',
            'password'
            ]
        extra_kwargs={
            'password':{'write_only':True}
            }
        
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
        email=attrs['email']
        password=attrs['password']
        user=authenticate(
            username=email,
            password=password
        )
        if user is None:
            raise serializers.ValidationError(
                "Invalid credentials"
            )
        refresh=RefreshToken.for_user(user)
        access=refresh.access_token
        return {
            'refresh': str(refresh),
            'access': str(access)
        }
        
class ProfileSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'email',
            'username',
            'profile_picture',
            'followers_count',
            'following_count'
        ]

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()
    
class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=User
        fields=['id','username']
        