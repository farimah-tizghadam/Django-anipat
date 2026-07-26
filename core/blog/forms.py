from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    """
    This is a form for post model
    """

    class Meta:
        model = Post
        fields = ["status", "title", "content", "image", "category", "published_date"]
