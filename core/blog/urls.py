from django.urls import path, include
from . import views

app_name = "blog"

urlpatterns = [
    path("post/", views.PostListView.as_view(), name="post-list"),
    path("post/api/", views.PostListApiView.as_view(), name="post-list-api"),
    path("post/create/", views.PostCreateView.as_view(), name="post-create"),
    path("post/<int:pk>/", views.PostDetailView.as_view(), name="post-detail"),
    path("post/<int:pk>/edit/", views.PostEditView.as_view(), name="post-edit"),
    path(
        "post/<int:pk>/delete/",
        views.PostDeleteView.as_view(),
        name="post-delete",
    ),
    path(
        "category/<str:cat_name>",
        views.PostsByCategoryView.as_view(),
        name="category",
    ),
    path(
        "tag/<str:tag_name>/",
        views.PostsByTagView.as_view(),
        name="posts-by-tag",
    ),
    path("search/", views.SearchView.as_view(), name="search"),
    # API
    path("api/v1/", include("blog.api.v1.urls")),
]
