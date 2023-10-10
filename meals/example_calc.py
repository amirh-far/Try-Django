from django.contrib.auth import get_user_model
from django.db.models import Sum
from recipes.models import RecipeIngredient
from .models import Meal

User = get_user_model
j = User.objects.first()

queue = Meal.objects.by_user(j).pending().prefetch_related("recipe__recipeingredient")
ids = queue.values_list("recipe__recipeingredient__id", flat=True)

qs = RecipeIngredient.objects.filter(id__in=ids)
data = qs.values("names", "unit").annotate(total=Sum("quntity_as_float"))
