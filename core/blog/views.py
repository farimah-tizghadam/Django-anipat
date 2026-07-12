from django.shortcuts import render
from .models import Post
from .forms import PostForm
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    FormView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)


class PostListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    """
    this is a CBV for getting the posts list.
    """
    queryset = Post.objects.filter(status=True)
    template_name = "blog/blog-home.html"
    context_object_name = "posts"
    paginate_by = 4

    permission_required = 'blog.view-post'




class PostDetailView(LoginRequiredMixin, DetailView):
    """
    CBV for getting post detail
    """

    model = Post
    context_object_name = "post"
    template_name = "blog/blog-single.html"



class PostCreateView(LoginRequiredMixin, CreateView):
    """
    CBV for creating post
    """

    model = Post
    form_class = PostForm
    success_url = reverse_lazy("blog:post-detail")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    


class PostEditView(LoginRequiredMixin, UpdateView):
    """
    CBV class for update/edit post
    """
    model = Post
    form_class = PostForm
    success_url = reverse_lazy("blog:post-list")


class PostDeleteView(LoginRequiredMixin, DeleteView):
    """
    CBV for Delete post
    """

    model = Post
    success_url = reverse_lazy("blog:post-list")
