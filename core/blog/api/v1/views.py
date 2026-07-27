from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
)
from rest_framework.response import Response
from rest_framework import viewsets

from .serializers import PostSerializer, CategorySerializer
from ...models import Post, Category
from accounts.models import Profile


class PostListCreateAPIView(ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    queryset = Post.objects.filter(status=True)

    def perform_create(self, serializer):
        profile = Profile.objects.get(user=self.request.user)
        serializer.save(author=profile)


class PostRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    queryset = Post.objects.filter(status=True)

    def retrieve(self, request, *args, **kwargs):
        post = self.get_object()
        post.increment_views()

        serializer = self.get_serializer(post)
        return Response(serializer.data)


class PostModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=True)
    # filterset_fields = ['author', 'category']
    search_fields = ["title", "content"]
    ordering_fields = ["published_date"]


class CategoryModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
