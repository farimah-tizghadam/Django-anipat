from rest_framework import serializers
from ...models import Post, Category
from accounts.models import Profile
from taggit.serializers import (TagListSerializerField, TaggitSerializer)


class PostSerializer(TaggitSerializer, serializers.ModelSerializer):
    
    tags = TagListSerializerField()
   
    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "title",
            "content",
            "image",
            "category",
            "status",
            "create_date",
            "published_date",
            "views",
            "tags",
        ]
        read_only_fields = ["author", "create_date", "views"]



    def get_tags(self, obj):
        return obj.tags.names()


        
class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ["id", "name"]