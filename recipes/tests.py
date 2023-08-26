from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import Recipe, RecipeIngredient
User = get_user_model()

class UserTestCase(TestCase):
    def setUp(self):
        self.user_a = User.objects.create_user("amirh-far", password="abc123")
    def test_user_pw(self):
        self.assertTrue(self.user_a.check_password("abc123"))


class RecipeTestCase(TestCase):
    def setUp(self):
        self.user_a = User.objects.create_user("amirh-far", password="abc123")
        self.recipe_a = Recipe.objects.create(
            user = self.user_a,
            name = "Grilled Chicken"
        )
        self.recipe_b = Recipe.objects.create(
            user = self.user_a,
            name = "Grilled Chicken Tacos"
        )
        self.recipe_ingredient_a = RecipeIngredient.objects.create(
            recipe = self.recipe_a,
            name = "Chicken",
            quantity = "1/2",
            unit = "pound"
        )
    def test_user_count(self):
        qs = User.objects.all()
        self.assertEqual(qs.count(), 1)

    def test_user_recipe_reverse_count(self):
        user = self.user_a
        qs = user.recipe_set.all() # Returns a query set
        # print(qs)
        self.assertEqual(qs.count(), 2)

    def test_user_recipe_forward_count(self):
        user = self.user_a
        qs = Recipe.objects.filter(user=user) # Returns a query set
        # print(qs)
        self.assertEqual(qs.count(), 2)

    def test_user_recipe_ingredient_reverse_count(self):
        recipe = self.recipe_a
        qs = recipe.recipeingredient_set.all() # Returns a query set
        # print(qs)
        self.assertEqual(qs.count(), 1)

    def test_user_recipe_ingredient_forward_count(self):
        recipe = self.recipe_a
        qs = RecipeIngredient.objects.filter(recipe=recipe) # Returns a query set
        # print(qs)
        self.assertEqual(qs.count(), 1)

    # This two level relation reverse is not recommended:
    def test_user_two_level_relation_reverse(self):
        user = self.user_a
        recipeingredient_ids = list(user.recipe_set.all().values_list(
            "recipeingredient__id", flat=True))
        # print(recipeingredient_ids)
        qs = RecipeIngredient.objects.filter(id__in=recipeingredient_ids)
        self.assertEqual(qs.count(), 1)

    # And this one is rarely used and its not recommended:
    def test_user_two_level_relation_via_recipes(self):
        user = self.user_a
        ids = user.recipe_set.all().values_list("id", flat=True)
        # print(ids)
        qs = RecipeIngredient.objects.filter(recipe__id__in=ids)
        # print(qs)
        self.assertEqual(qs.count(), 1)
    
    def test_unit_measure_validation_error(self):
        invalid_units = ["nada", "dasda"]
        with self.assertRaises(ValidationError):
            for unit in invalid_units:
                ingredient = RecipeIngredient.objects.create(
                    recipe = self.recipe_a,
                    name = "New",
                    quantity = 10,
                    unit = unit,
                )
                ingredient.full_clean()

    def test_unit_measure_validation(self):
        valid_unit = "ounce"
        ingredient = RecipeIngredient.objects.create(
            recipe = self.recipe_a,
            name = "New",
            quantity = 10,
            unit = valid_unit,
            )
        ingredient.full_clean()