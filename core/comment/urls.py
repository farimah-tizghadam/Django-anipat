from django.urls import path
from . import views

app_name = "comment"

urlpatterns = [
    path(
        "create/<int:pk>/",
        views.CommentCreateView.as_view(),
        name="comment-create",
    ),
]
