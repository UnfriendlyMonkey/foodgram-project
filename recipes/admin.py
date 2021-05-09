from django.contrib import admin
from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag, Follow


class RecipeIngredientInline(admin.TabularInline):
	model = RecipeIngredient
	extra = 1

#
# class RecipeTagInline(admin.TabularInline):
# 	model = Tag
# 	extra = 1


class RecipeAdmin(admin.ModelAdmin):
	inlines = [
		RecipeIngredientInline,
	]


admin.site.register(Ingredient)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient)
admin.site.register(Tag)
admin.site.register(Follow)
