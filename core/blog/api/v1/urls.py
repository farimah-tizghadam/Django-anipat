from django.urls import path
from . import views


app_name = 'api-v1'

urlpatterns = [
    path("post/",views.PostListCreateAPIView.as_view(), name="post-list"),
    path("post/<int:pk>/",views.PostRetrieveUpdateDestroyAPIView.as_view(), name="post-detail"),
]