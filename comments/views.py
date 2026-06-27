from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Comment
from .serializers import CommentSerializer


class CreateCommentView(APIView):
    permission_classes=[IsAuthenticated]
    
    def post(self,request):
        serializer=CommentSerializer(data=request.data)
        
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

class ListCommentView(APIView):
    permission_classes=[IsAuthenticated]
    
    def get(self,request):
        comments=Comment.objects.all()
        serializer=CommentSerializer(
            comments,
            many=True
            )
        return Response(serializer.data)

class UpdateCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, id):
        try:
            comment = Comment.objects.get(id=id)
        except Comment.DoesNotExist:
            return Response(
                {"error": "Comment not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if request.user != comment.user:
            return Response(
                {"error": "Forbidden"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer=CommentSerializer(
            comment,
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
        
class DeleteCommentView(APIView):
    permission_classes=[IsAuthenticated]
    
    def delete(self, request, id):
        try:
            comment = Comment.objects.get(id=id)
        except Comment.DoesNotExist:
            return Response(
                {"error": "Comment not found"},
                status=status.HTTP_404_NOT_FOUND
        )
        if request.user != comment.user:
            return Response(
                {"error": "Forbidden"},
                status=status.HTTP_403_FORBIDDEN
            )
        comment.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )