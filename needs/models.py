from django.db import models
from django.core import validators 
# Create your models here.
class Needs(models.Model):
    sentence = models.TextField(unique=True)
    date = models.DateTimeField()
    label = models.IntegerField(default=None,null=True,validators=[validators.MinValueValidator(0),validators.MaxValueValidator(1)])
    negative = models.FloatField()
    positive = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)