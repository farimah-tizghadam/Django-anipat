from django.contrib import admin
from .models import Comment

# Register your models here


class CommentAdmin(admin.ModelAdmin):
    date_hierarchy = "creation_date"
    list_display = [
        "name",
        "email",
        "approved",
        "updated_date",
        "creation_date",
    ]
    list_filter = ("approved",)
    search_fields = ["subject", "message"]


admin.site.register(Comment, CommentAdmin)
