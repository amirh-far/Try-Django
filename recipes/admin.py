from django.contrib import admin
from .models import Recipe, RecipeIngredient, RecipeIngredientImage

admin.site.register(RecipeIngredientImage)

class RecipeIngredientInline(admin.StackedInline):
    model = RecipeIngredient
    extra = 0
    readonly_fields = ["quantity_as_float", "as_mks", "as_imperial"]
admin.site.register(RecipeIngredient)

class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInline]
    list_display = ["name","description", "user"]
    readonly_fields = ["timestamp", "updated"]
    raw_id_fields = ["user"]

admin.site.register(Recipe, RecipeAdmin)

