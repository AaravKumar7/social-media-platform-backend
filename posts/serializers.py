from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id',
            'user',
            'content',
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