from django.contrib import admin
from .models import Contact, NewsLetter

# Register your models here.


class ContactAdmin(admin.ModelAdmin):
    date_hierarchy = "creation_date"
    list_display = ["name", "email", "subject", "creation_date"]
    list_filter = ["name", "email"]
    search_fields = ["name", "message"]


admin.site.register(Contact, ContactAdmin)
admin.site.register(NewsLetter)
