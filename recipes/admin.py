from django.contrib import admin
from recipes.models import Ingredient, Recipe, RecipeIngredient


class RecipeIngredientInline(admin.TabularInline):
	model = RecipeIngredient
	extra = 1


class RecipeAdmin(admin.ModelAdmin):
	inlines = [RecipeIngredientInline]


admin.site.register(Ingredient)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient)
