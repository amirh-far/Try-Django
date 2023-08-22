from django.db import models
from django.utils import timezone
# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=70)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    publish = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True, default=timezone.now)
    # null=True means that the data field can be STORED empty 
    # The blank=True means that the form can be accepted empty
