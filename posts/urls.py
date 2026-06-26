from django.urls import path
from .views import (
    CreatePostView,
    ListPostView,
    UpdatePostView,
    DeletePostView,
    ToggleLikeView,
)

urlpatterns = [
    path('create/', CreatePostView.as_view(), name='create-post'),
    path('', ListPostView.as_view(), name='list-posts'),
    path('<int:id>/', UpdatePostView.as_view(), name='update-post'),
    path('<int:id>/delete/', DeletePostView.as_view(), name='delete-post'),
    path('<int:id>/like/', ToggleLikeView.as_view(), name='toggle-like'),
]