from django.db import models
from django.conf import settings
from django.urls import reverse

from recipes.models import Recipe

User = settings.AUTH_USER_MODEL

class MealStatus(models.TextChoices):
    PENDING = "p", "Pending"
    COMPLETED = "c", "Completed"
    EXPIRED = "e", "Expired"
    ABORTED = "a", "Aborted"

# MEAL_CHOICES = 

class MealQuerySet(models.QuerySet):
    def by_user_id(self, user_id):
        return self.filter(user_id=user_id)
    
    def by_user_id(self, user):
        return self.filter(user=user)
    
    def pending(self):
        return self.filter(status=MealStatus.PENDING)
    
    def completed(self):
        return self.filter(status=MealStatus.COMPLETED)
    
    def expired(self):
        return self.filter(status=MealStatus.EXPIRED)
    
    def aborted(self):
        return self.filter(status=MealStatus.ABORTED)
    
class MealManager(models.Manager):
    def get_queryset(self):
            return MealQuerySet(self.model, using=self._db)
 

class Meal(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, choices=MealStatus.choices, default=MealStatus.PENDING)

    objects = MealManager()

