from django.urls import path
from .views import RegisterView, LoginView, ProfileView, ToggleFollowView, SearchUserView, UpdateProfilePictureView

urlpatterns = [
    path(
        'register/',
        RegisterView.as_view(),
        name='register'
        ),
    path(
        'login/',
        LoginView.as_view(),
        name='login'
        ),
    path(
        'profile/',
        ProfileView.as_view(),
        name='profile'
        ),
    path(
        'follow/<int:id>/',
        ToggleFollowView.as_view(),
        name='toggle-follow'
        ),
    path(
        'search/', 
        SearchUserView.as_view(), 
        name='search-user'
        ),
    path(
        'profile/picture/',UpdateProfilePictureView.as_view(),
        name='update-profile-picture'
    ),
]