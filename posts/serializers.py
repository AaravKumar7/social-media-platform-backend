from rest_framework import serializers
from .models import Post
from users.serializers import UserSerializer

class PostSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id',
            'user',
            'content',
            'image',
            'likes_count',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'user',
            'created_at',
            'updated_at'
        ]

    def get_likes_count(self, obj):
        return obj.likes.count()