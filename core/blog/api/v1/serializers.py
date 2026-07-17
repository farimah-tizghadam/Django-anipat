from rest_framework import serializers
from ...models import Post


class PostSerializer(serializers.ModelSerializer):
   
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
            "published_date",
        ]
        read_only_fields = ["author", "create_date"]



        
