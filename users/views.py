from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import RegisterSerializer, LoginSerializer, ProfileSerializer
from django.contrib.auth import get_user_model

class RegisterView(APIView):
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, 
                status=status.HTTP_201_CREATED
                )
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
            )
        
class LoginView(APIView):
    
    def post(self,request):
        serializer=LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(
                serializer.validated_data,
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
        
class ProfileView(APIView):
    permission_classes=[IsAuthenticated]
    
    def get(self, request):
        user=request.user
        serializer=ProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

User=get_user_model()

class ToggleFollowView(APIView):
    permission_classes=[IsAuthenticated]
    
    def post(self,request,id):
        user=request.user
        serializer=ProfileSerializer(user)
        try:
            target_user=User.objects.get(id=id)
        except User.DoesNotExist:
            return Response(
                {"error":"User not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        if request.user==target_user:
            return Response(
                {"error":"You cannot follow yourself"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if request.user.following.filter(id=target_user.id).exists():
            request.user.following.remove(target_user)

            return Response(
                {
                    "following": False,
                    "followers_count": target_user.followers.count(),
                    "following_count": request.user.following.count(),
                    "message": "User unfollowed"
                },
                status=status.HTTP_200_OK
            )

        request.user.following.add(target_user)

        return Response(
        {
            "following": True,
            "followers_count": target_user.followers.count(),
            "following_count": request.user.following.count(),
            "message": "User followed"
        },
        status=status.HTTP_200_OK
    )