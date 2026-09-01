from .models import Post, Category
from comment.forms import CommentForm
from taggit.models import Tag
from .forms import PostForm
from django.urls import reverse_lazy
from django.db.models import Q
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
)
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.core.cache import cache
from django.urls import reverse


class PopularPostsMixin:
    post_limit = 4

    def get_popular_posts(self):
        key = "blog:popular_posts"
        posts = cache.get(key)
        if posts is None:
            posts = Post.objects.filter(status=True)
            posts = posts.order_by("-views", "-published_date")[: self.post_limit]
            cache.set(key, posts, timeout=60 * 5)
        return posts

    def get_categories(self):
        key = "blog:categories"
        categories = cache.get(key)

        if categories is None:
            categories = (
                Category.objects.filter(post__status=True).distinct().order_by("name")
            )
            cache.set(key, categories, timeout=60 * 5)

        return categories

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["popular_posts"] = self.get_popular_posts()
        context["tags"] = Tag.objects.all()
        context["categories"] = self.get_categories()

        return context


@method_decorator(never_cache, name="dispatch")
class PostListView(LoginRequiredMixin, PopularPostsMixin, ListView):
    """
    this is a CBV for getting the posts list.
    """

    queryset = Post.objects.filter(status=True)
    template_name = "blog/blog-home.html"
    context_object_name = "posts"
    paginate_by = 3

    permission_required = "blog.view_post"


class PostListApiView(TemplateView):
    template_name = "blog/post-list-api.html"


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
                status=True, published_date__lt=self.object.published_date
            )
            .order_by("-published_date")
            .first()
        )

        context["next_post"] = (
            Post.objects.filter(
                status=True, published_date__gt=self.object.published_date
            )
            .order_by("published_date")
            .first()
        )

        context["comment_form"] = CommentForm()
        context["comments"] = self.object.comments.filter(
            parent__isnull=True, approved=True
        )

        return context


class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    CBV for creating post
    """

    model = Post
    form_class = PostForm
    permission_required = "blog.add_post"

    POPULAR_POSTS_CACHE_KEY = "blog:popular_posts"

    def form_valid(self, form):

        profile = self.request.user.profile_set.first()
        form.instance.author = profile
        response = super().form_valid(form)
        return response

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse(
            "blog:post-detail",
            kwargs={"pk": self.object.pk},
        )


class PostEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    CBV class for update/edit post
    """

    model = Post
    form_class = PostForm
    success_url = reverse_lazy("blog:post-list")

    POPULAR_POSTS_CACHE_KEY = "blog:popular_posts"

    # This func prevents user to manually change the URL from
    def test_func(self):
        post = self.get_object()
        return post.author.user == self.request.user


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    CBV for Delete post
    """

    model = Post
    success_url = reverse_lazy("blog:post-list")

    cache.delete("popular_posts")
    POPULAR_POSTS_CACHE_KEY = "blog:popular_posts"

    # This func prevents user to manually change the URL from
    def test_func(self):
        post = self.get_object()
        return post.author.user == self.request.user


@method_decorator(never_cache, name="dispatch")
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
            Q(title__icontains=query) | Q(content__icontains=query),
            status=True,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q", "")
        return context
