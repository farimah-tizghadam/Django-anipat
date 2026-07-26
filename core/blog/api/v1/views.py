from rest_framework.decorators import api_view
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets

from .serializers import PostSerializer, CategorySerializer
from django.shortcuts import get_object_or_404
from ...models import Post, Category
from accounts.models import Profile

# @api_view(["GET","POST"])
# def PostList(request):
#     if request.method == "GET":
#         post = Post.objects.filter(status=True)
#         serializer = PostSerializer(post, many=True)
#         return Response(serializer.data)
#     elif request.method == "POST":
#         serializer = PostSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)


# @api_view()
# def PostDetail(request, id):
#     post = get_object_or_404(Post,pk=id, status=True)
#     serializer = PostSerializer(post)
#     return Response(serializer.data)


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
