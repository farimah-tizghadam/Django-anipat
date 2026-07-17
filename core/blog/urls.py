from django.urls import path, include
from django.views.generic import TemplateView
from . import views


app_name = 'blog'

urlpatterns = [
    path("post/", views.PostListView.as_view(), name="post-list"),
    path("post/create/", views.PostCreateView.as_view(), name="post-create"),
    path("post/<int:pk>/", views.PostDetailView.as_view(), name="post-detail"),
    path("post/<int:pk>/edit/", views.PostEditView.as_view(), name="post-edit"),
    path("post/<int:pk>/delete/", views.PostDeleteView.as_view(), name="post-delete"),
    #API
    path("api/v1/", include("blog.api.v1.urls")),

]