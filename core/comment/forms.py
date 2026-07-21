from django import forms
from .models import Comment




class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["message", "name", "email"]
        widgets = {
            "message": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "leave a comment....",
                }
            )
        }