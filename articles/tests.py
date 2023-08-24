from django.test import TestCase
from .models import Article
from django.utils.text import slugify
from .utils import slugify_instance_title
# Create your tests here.

class ArticleTestCase(TestCase):
    def setUp(self):
        self.article_obj_count = 2_000
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

    def test_slugify_instance_title(self):
        obj = Article.objects.all().last()
        new_slugs = []
        for _ in range(25):
            instance = slugify_instance_title(obj, save=False)
            new_slugs.append(instance.slug)

        unique_slugs = list(set(new_slugs))
        self.assertEqual(len(new_slugs), len(unique_slugs))

    def test_slugify_instance_title_redux(self):
        slugs_list = Article.objects.all().values_list("slug", flat=True)
        unique_slugs_list = list(set(slugs_list))
        self.assertEqual(len(slugs_list), len(unique_slugs_list))

    # def test_user_created_instance(self):
    #     obj = Article.objects.create(title="Hello World", content="Tiamo")
    #     qs = Article.objects.all()
    #     for o in qs:
    #         self.assertNotEqual(obj.slug, o.slug)
    def test_article_search_manager(self):
        qs = Article.objects.search(query="Hello world")
        self.assertEqual(qs.count(), self.article_obj_count)
        qs = Article.objects.search(query="hello")
        self.assertEqual(qs.count(), self.article_obj_count)
        qs = Article.objects.search(query="Mew")
        self.assertEqual(qs.count(), self.article_obj_count)
        

    
