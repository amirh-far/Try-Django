from django.db import models
from django.db.models import Q
from django.db.models.query import QuerySet
from django.db.models.signals import pre_save, post_save
from django.urls import reverse
from django.conf import settings
# from django.utils import timezone
# import datetime

from articles.utils import slugify_instance_title

User = settings.AUTH_USER_MODEL


class ArticleQuerySet(models.QuerySet):
    def search(self, query=None):
        if query is None:
            return self.none() # []
        lookups = Q(title__icontains=query) | Q(content__icontains=query)
        return self.filter(lookups)


class ArticleManager(models.Manager):
    def get_queryset(self):
            return ArticleQuerySet(self.model, using=self._db)
    
    def search(self, query=None):
        return self.get_queryset().search(query=query)


class Article(models.Model):

    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=70)
    content = models.TextField()
    slug = models.SlugField(unique=True, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    publish = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    # null=True means that the data field can be STORED empty 
    # The blank=True means that the form can be accepted empty
    
    objects = ArticleManager()

    def get_absolute_url(self):
        # return f"/articles/{self.slug}/"
        return reverse("article-detail", kwargs={"slug": self.slug})


    def save(self, *args, **kwargs):
        # Overriding the save method
        # what we did using save previously:
        # obj = Article.objects.get(id=1)
        # obj.save()
        # if self.slug is None:
            # self.slug = slugify(self.title)


        super().save(*args, **kwargs)


def article_pre_save(sender, instance, *args, **kwargs):
    # print("pre_save")
    # print(args, kwargs)
    # print(instance.slug is None) 
    if instance.slug is None:
        slugify_instance_title(instance, save=False)

pre_save.connect(article_pre_save,sender=Article)


def article_post_save(sender, instance, created, *args, **kwargs):
    # print("post_save")
    # print(args, kwargs) 
    # print(created)
    if created:
        slugify_instance_title(instance, save=True)

post_save.connect(article_post_save, sender=Article)


# for obj in Article.objects.all():
#     obj.slug = None
#     obj.save()
