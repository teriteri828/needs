from django.db import models

# Create your models here.
class Needs(models.Model):
    sentences = models.TextField()
    date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)