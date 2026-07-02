from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import PostSerializer
from .models import Post
from .pagination import PostPagination
from rest_framework.parsers import MultiPartParser, FormParser

class CreatePostView(APIView):
    permission_classes=[IsAuthenticated]
    parser_classes=[MultiPartParser, FormParser]
    
    def post(self,request):
        serializer=PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
        
class ListPostView(APIView):
    permission_classes=[IsAuthenticated]
    
    def get(self,request):
        posts=Post.objects.select_related('user').prefetch_related('likes').order_by('-created_at')
        paginator=PostPagination()
        page=paginator.paginate_queryset(posts,request)
        serializer=PostSerializer(page,many=True)
        return paginator.get_paginated_response(serializer.data)
    
class UpdatePostView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self,request,id):
        try:
            post = Post.objects.get(id=id)
        except Post.DoesNotExist:
            return Response(
                {"error": "Post not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if request.user != post.user:
            return Response(
                {"error": "Forbidden"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = PostSerializer(
            post,
            data=request.data
            )

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
        
class DeletePostView(APIView):
    permission_classes=[IsAuthenticated]
    
    def delete(self, request, id):
        try:
            post = Post.objects.get(id=id)
        except Post.DoesNotExist:
            return Response(
                {"error": "Post not found"},
                status=status.HTTP_404_NOT_FOUND
        )
        if request.user!=post.user:
            return Response(
                {"error": "Forbidden"},
                status=status.HTTP_403_FORBIDDEN
            )
        post.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
    
class ToggleLikeView(APIView):
    permission_classes=[IsAuthenticated]
    
    def post(self,request,id):
        try:
            post=Post.objects.get(id=id)
        except Post.DoesNotExist:
            return Response(
                {'error':"Post not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)

            return Response(
                {
                    "liked":False,
                    "likes_count":post.likes.count(),
                    "message": "Post unliked"
                },
                status=status.HTTP_200_OK
            )

        post.likes.add(request.user)

        return Response(
            {
                "liked":True,
                "likes_count":post.likes.count(),
                "message": "Post liked"
            },
            status=status.HTTP_200_OK
        )

class FeedView(APIView):
    permission_classes=[IsAuthenticated]
    
    def get(self,request):
        following_ids=request.user.following.values_list(
            'id',
            flat=True
        )
        following_ids=list(following_ids)
        following_ids.append(request.user.id)
        posts=Post.objects.select_related('user').prefetch_related('likes').filter(
            user__id__in=following_ids
        ).order_by('-created_at')
        serializer=PostSerializer(posts,many=True)
        return Response(serializer.data)
    
class SearchPostView(APIView):
    permission_classes=[IsAuthenticated]
    
    def get(self,request):
        query=request.query_params.get('q','')
        posts=Post.objects.select_related('user').prefetch_related('likes').filter(
            content__icontains=query
        )
        serializer=PostSerializer(posts,many=True)
        return Response(
            serializer.data
        )