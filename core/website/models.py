from django.db import models

# Create your models here.


class Contact(models.Model):
    name = models.CharField(max_length=225)
    email = models.EmailField()
    subject = models.CharField(max_length=225, null=True, blank=True)
    message = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["creation_date"]

    def __str__(self):
        return self.name


class NewsLetter(models.Model):
    email = models.EmailField()

    def __str__(self):
        return self.email
