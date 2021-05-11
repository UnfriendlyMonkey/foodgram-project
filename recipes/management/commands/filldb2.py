from random import randint, sample

from django.core.management.base import BaseCommand

from ...models import Recipe, User, ShoppingCart, Follow

MAX_FAVORITES = 20
MAX_FOLLOWINGS = 40


class Command(BaseCommand):
    """Custom `filldb2` command
    """
    help = 'Fill DB with additional data'

    def handle(self, *args, **options):

        for user in User.objects.all():
            recipes = list(Recipe.objects.all())
            to_shopping_cart = sample(recipes, k=randint(1, MAX_FAVORITES))
            ShoppingCart.objects.bulk_create([
                ShoppingCart(user=user, recipe=recipe) for recipe in to_shopping_cart
            ])
            other_users = list(User.objects.exclude(username=user.username))
            to_followings = sample(other_users, k=randint(1, MAX_FOLLOWINGS))
            Follow.objects.bulk_create([
                Follow(follower=user, following=person) for person in to_followings
            ])
