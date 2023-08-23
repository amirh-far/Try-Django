from django.db import models
from django.db.models.signals import pre_save, post_save

from django.utils import timezone
import datetime
from django.utils.text import slugify
# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=70)
    content = models.TextField()
    slug = models.SlugField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    publish = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    # null=True means that the data field can be STORED empty 
    # The blank=True means that the form can be accepted empty

    def save(self, *args, **kwargs):
        # Overriding the save method
        # what we did using save previously:
        # obj = Article.objects.get(id=1)
        # obj.save()
        # if self.slug is None:
            # self.slug = slugify(self.title)


        super().save(*args, **kwargs)


def slugify_instance_title(instance, save=False):
    slug = slugify(instance.title)
    instance.slug = slug
    qs = Article.objects.filter(slug=slug).exclude(id=instance.id) # we exclude the current item because we dont want to check it
    print(qs.exists())
    if qs.exists():
        slug = f"{slug}-{qs.count() + 1}"
    instance.slug = slug
    if save:
        instance.save()
    return instance

def article_pre_save(sender, instance, *args, **kwargs):
    print("pre_save")
    # print(args, kwargs)
    # print(instance.slug is None) 
    if instance.slug is None:
        slugify_instance_title(instance, save=False)

pre_save.connect(article_pre_save,sender=Article)


def article_post_save(sender, instance, created, *args, **kwargs):
    print("post_save")
    # print(args, kwargs) 
    # print(created)
    if created:
        slugify_instance_title(instance, save=True)

post_save.connect(article_post_save, sender=Article)


for obj in Article.objects.all():
    obj.slug = None
    obj.save()
