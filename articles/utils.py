import random
from django.utils.text import slugify

def slugify_instance_title(instance, save=False, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)
    Klass = instance.__class__
    qs = Klass.objects.filter(slug=slug).exclude(id=instance.id) # we exclude the current item because we dont want to check it
    if qs.exists():
        slug = f"{slug}-{random.randint(0,100_000)}"
        return slugify_instance_title(instance, save=save, new_slug=slug)
    instance.slug = slug
    if save:
        instance.save()
    return instance


# This method has a problem that if you create a new article obj because the other slugs are created and they are unique,
# when it does .exists, it returns 1 and there is only one of them exacly like that and it doesnt know that the other slugs already exist:
# def slugify_instance_title(instance, save=False):
#     slug = slugify(instance.title)
#     qs = Article.objects.filter(slug=slug).exclude(id=instance.id) # we exclude the current item because we dont want to check it
#     print(qs.exists())
#     if qs.exists():
#         slug = f"{slug}-{qs.count() + 1}"
#     instance.slug = slug
#     if save:
#         instance.save()
#     return instance
    