from django.shortcuts import render
from .models import Post, Category
from taggit.models import Tag
from .forms import PostForm
from django.urls import reverse_lazy
from django.db.models import Q
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
from django.shortcuts import get_object_or_404



class PopularPostsMixin:
    post_limit = 4
    def get_popular_posts(self):
        posts = Post.objects.filter(status=True)
        posts = posts.order_by("-views", "-published_date")[:self.post_limit]
        return posts

    def get_categories(self):
        categories = Category.objects.filter(post__status=True).distinct().order_by("name")
        return categories

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["popular_posts"] = self.get_popular_posts()
        context["tags"] = Tag.objects.all()
        context["categories"] = self.get_categories()

        return context



class PostListView(PermissionRequiredMixin, LoginRequiredMixin, PopularPostsMixin, ListView):
    """
    this is a CBV for getting the posts list.
    """
    queryset = Post.objects.filter(status=True)
    template_name = "blog/blog-home.html"
    context_object_name = "posts"
    paginate_by = 3

    permission_required = 'blog.view_post'




class PostDetailView(LoginRequiredMixin, PopularPostsMixin, DetailView):
    """
    CBV for getting post detail
    """

    model = Post
    context_object_name = "post"
    template_name = "blog/blog-single.html"


    def get_object(self, queryset=None):
        post = super().get_object(queryset)
        post.increment_views()
        return post


    def get_context_data(self, **kwargs):
        # finds the newest post published before the current one or via versa
        context = super().get_context_data(**kwargs)

        context["previous_post"] = (
            Post.objects.filter(
                status=True,
                published_date__lt=self.object.published_date
            )
            .order_by("-published_date")
            .first()
        )

        context["next_post"] = (
            Post.objects.filter(
                status=True,
                published_date__gt=self.object.published_date
            )
            .order_by("published_date")
            .first()
        )

        return context


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


class PostsByTagView(LoginRequiredMixin, PopularPostsMixin, ListView):
    """
    filtering posts by selected tag.
    """

    template_name = "blog/blog-home.html"
    context_object_name = "posts"
    paginate_by = 4

    def get_queryset(self):
        tag = get_object_or_404(Tag, slug=self.kwargs["tag_name"])
        return Post.objects.filter(status=True, tags=tag)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tag"] = get_object_or_404(Tag, slug=self.kwargs["tag_name"])
        return context


class PostsByCategoryView(LoginRequiredMixin, PopularPostsMixin, ListView):
    """
    filtering posts by category
    """
     
    template_name = "blog/blog-home.html"
    context_object_name = "posts"
    paginate_by = 4

    def get_queryset(self):
        self.category = get_object_or_404(Category, name=self.kwargs["cat_name"])
        return Post.objects.filter(
            status=True,
            category=self.category,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        return context
    


class SearchView(LoginRequiredMixin, PopularPostsMixin, ListView):

    template_name = "blog/blog-home.html"
    context_object_name = "posts"
    paginate_by = 4

    def get_queryset(self):
        query = self.request.GET.get("q", "")

        if not query:
            return Post.objects.filter(status=True)
        
        return Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query),
            status=True,
        )


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q", "")
        return context