from random import randint, sample

from django.core.management.base import BaseCommand

from users.factories import UserFactory

from ...factories import RecipeFactory
from ...models import Favorite, Recipe, User

USERS = 100
MAX_RECIPES = 10
MAX_FAVORITES = 20


class Command(BaseCommand):
    """Custom `filldb` command
    """
    help = 'Fill DB with sample data'

    def handle(self, *args, **options):
        users = UserFactory.create_batch(USERS)

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
