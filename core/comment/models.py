from django.db import models
from blog.models import Post

class Comment(models.Model):
    name = models.CharField(max_length=225)
    email = models.EmailField()
    subject = models.CharField(max_length=225, null=True, blank=True)
    message = models.TextField()
    approved = models.BooleanField(default=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name="replies")


    creation_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-creation_date']


    def __str__(self):
        return f"{self.id}"