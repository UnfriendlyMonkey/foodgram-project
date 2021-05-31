from django.contrib import admin
from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag, Follow, Favorite, ShoppingCart


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit',)
    search_fields = ('name',)
    list_filter = ('name', 'unit',)


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    fields = ('ingredient', 'recipe', 'quantity',)
    search_fields = ('ingredient__name', 'recipe__title',)


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1
    min_num = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    def favorites_count(self, item):
        return item.favorites.count()
    favorites_count.short_description = 'В избранном'
    list_display = ('title', 'user', 'pub_date', 'cooking_time', 'favorites_count')
    search_fields = ('title', 'user__username')
    list_filter = ('user', 'tag', 'title')
    autocomplete_fields = ('ingredient',)
    inlines = (RecipeIngredientInline,)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    fields = ('user', 'recipe',)
    search_fields = ('user__username', 'recipe__title',)


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    fields = ('user', 'recipe',)
    search_fields = ('user__username', 'recipe__title',)


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    fields = ('follower', 'following',)
    search_fields = ('follower__username', 'following__username')


admin.site.register(Tag)
