from django.urls import path
from .views import CreateCommentView, ListCommentView, UpdateCommentView, DeleteCommentView

urlpatterns = [
    path(
        'create/',
        CreateCommentView.as_view(),
        name='create-comment'
        ),
    path(
        '',
        ListCommentView.as_view(),
        name='list-comments'
        ),
    path(
        '<int:id>/',
        UpdateCommentView.as_view(),
        name='update-comment'
        ),
    path(
        '<int:id>/delete/',
        DeleteCommentView.as_view(),
        name='delete-comment'
        ),
]