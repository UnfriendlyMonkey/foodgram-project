from random import randint, sample

from django.core.management.base import BaseCommand

from users.factories import UserFactory

from ...factories import RecipeFactory
from ...models import Favorite, Recipe, User, Tag, RecipeIngredient, ShoppingCart, Ingredient, Follow

USERS = 100
MAX_RECIPES = 10
MAX_FAVORITES = 20


class Command(BaseCommand):
    """Custom `filldb` command
    """
    help = 'Fill DB with sample data'

    def handle(self, *args, **options):
        users = UserFactory.create_batch(USERS)
        tags = Tag.objects.all()
        ing = Ingredient.objects.all()

        for user in users:
            for _ in range(randint(0, MAX_RECIPES)):
                RecipeFactory(user=user)

        for user in User.objects.all():
            # User cannot favorite his own recipes
            recipes = list(Recipe.objects.exclude(user=user))
            to_favorite = sample(recipes, k=randint(1, MAX_FAVORITES))
            Favorite.objects.bulk_create([
                Favorite(user=user, recipe=recipe) for recipe in to_favorite
            ])

        for user in User.objects.all():
            recipes = list(Recipe.objects.all())
            to_shopping_cart = sample(recipes, k=randint(1, MAX_FAVORITES))
            ShoppingCart.objects.bulk_create([
                ShoppingCart(user=user, recipe=recipe) for recipe in to_shopping_cart
            ])

        for user in User.objects.all():
            other_users = list(User.objects.exclude(username=user.username))
            to_followings = sample(other_users, k=randint(1, MAX_FAVORITES))
            Follow.objects.bulk_create([
                Follow(follower=user, following=person) for person in to_followings
            ])

        for recipe in Recipe.objects.all():
            recipe.tag.add(tags[randint(0, 2)])
            q = randint(1, 4)
            ing_to_add = sample(list(ing), q)
            for i in ing_to_add:
                rp = RecipeIngredient.objects.create(recipe=recipe, ingredient=i, quantity=randint(50, 500))
                rp.save()
