from django.test import TestCase
from .models import Article
from django.utils.text import slugify
# Create your tests here.

class ArticleTestCase(TestCase):
    def setUp(self):
        self.article_obj_count = 5
        for _ in range(self.article_obj_count):
            Article.objects.create(title="Hello world", content="Mew Mew")

    def test_queryset_exists(self):
        qs = Article.objects.all()
        self.assertTrue(qs.exists())

    def test_queryset_count(self):
        qs = Article.objects.all()
        self.assertEqual(qs.count(), self.article_obj_count)

    def test_hello_world_slug(self):
        obj = Article.objects.all().order_by("id").first()
        self.assertEqual(obj.slug, slugify(obj.title))

    def test_hello_world_unique_slug(self):
        qs = Article.objects.exclude(slug__iexact="hello-world")
        for obj in qs:
            self.assertNotEqual(obj.slug, slugify(obj.title))
