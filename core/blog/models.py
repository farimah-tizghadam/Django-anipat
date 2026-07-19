from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import F
from taggit.managers import TaggableManager


# getting user model object
User = get_user_model()

class Post(models.Model):
    '''
    this is a class to define posts for blog app
    '''

    author = models.ForeignKey("accounts.Profile", on_delete=models.CASCADE)
    image = models.ImageField(null=True,blank=True)
    title = models.CharField(max_length=250)
    content = models.TextField()
    status = models.BooleanField()
    category = models.ForeignKey('Category',on_delete=models.SET_NULL,null=True)
    views= models.BigIntegerField(default = 0)
    tags = TaggableManager(blank=True)

    create_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField()

    def __str__(self):
        return self.title
    
    def increment_views(self):
        Post.objects.filter(pk=self.pk).update(views=F("views") + 1) #using F() increment directly and avoids losing counts when requests happen at the same time.
        self.refresh_from_db(fields=["views"])

    

class Category(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name