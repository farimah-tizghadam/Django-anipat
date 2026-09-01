from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    """
    This is a form for post model
    """
    class Meta:
        model = Post

        fields = [
            "status",
            "title",
            "content",
            "image",
            "category",
            "tags",
            "published_date",
        ]

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter post title",
                }
            ),

            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 8,
                    "placeholder": "Write your post...",
                }
            ),

            "category": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "tags": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "dog, cat, pet care",
                }
            ),

            "image": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                }
            ),
        }