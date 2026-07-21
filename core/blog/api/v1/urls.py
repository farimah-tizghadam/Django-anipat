from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter


app_name = 'api-v1'

router = DefaultRouter()
router.register("post", views.PostModelViewSet, basename="post")
router.register("category", views.CategoryModelViewSet, basename="category")
urlpatterns = router.urls



# urlpatterns = [
#     path("post/",views.PostListCreateAPIView.as_view(), name="post-list"),
#     path("post/<int:pk>/",views.PostRetrieveUpdateDestroyAPIView.as_view(), name="post-detail"),
# ]