from django.contrib.auth import get_user_model
from django.db.models import Sum
from recipes.models import RecipeIngredient
from .models import Meal

User = get_user_model
j = User.objects.first()
def generate_meal_queue_totals(user):  
    queue = Meal.objects.get_queue(user, prefetch_ingredients=True)
    ids = queue.values_list("recipe__recipeingredient__id", flat=True)
    qs = RecipeIngredient.objects.filter(id__in=ids)
    return qs.values("names", "unit").annotate(total=Sum("quntity_as_float")) 

