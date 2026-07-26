from django.shortcuts import render
from django.views import View
from .forms import CommentForm
from .models import Comment
from blog.models import Post
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Prefetch
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

# Create your views here.


class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk, status=True)

        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user

            comment.save()
            messages.add_message(
                request, messages.SUCCESS, "Your message submited successfully "
            )
        else:
            messages.add_message(
                request, messages.ERROR, "Your message didn't submited successfully"
            )

        return redirect("blog:post-detail", pk=post.pk)
