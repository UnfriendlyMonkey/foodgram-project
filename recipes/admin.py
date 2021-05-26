from django.contrib import admin
from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag, Follow, Favorite, ShoppingCart


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit',)
    search_fields = ('name',)
    list_filter = ('unit',)


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    fields = ('ingredient', 'recipe', 'quantity',)
    search_fields = ('ingredient', 'recipe',)


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1
    min_num = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'pub_date',)
    search_fields = ('title',)
    list_filter = ('user',)
    autocomplete_fields = ('ingredient',)
    inlines = (RecipeIngredientInline,)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    fields = ('user', 'recipe',)
    search_fields = ('user', 'recipe',)


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    fields = ('user', 'recipe',)
    search_fields = ('user', 'recipe',)


admin.site.register(Tag)
admin.site.register(Follow)
