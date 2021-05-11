from random import choice, randint

import factory
from factory import fuzzy

from users.factories import UserFactory

from recipes import models


class BaseRecipeFactory(factory.django.DjangoModelFactory):
    """Factory that generates Recipes without Ingredients."""
    user = factory.SubFactory(UserFactory)
    title = factory.Faker('word')
    slug = title
    image = factory.django.ImageField(width=1000)
    description = factory.Faker('text')
    # no ingredients
    cooking_time = fuzzy.FuzzyInteger(10, 120)
    tag = factory.Iterator(models.Tag.objects.all())

    class Meta:
        model = models.Recipe


class RecipeIngredientFactory(factory.django.DjangoModelFactory):
    """Factory that generates Recipes with Ingredients."""
    recipe = factory.SubFactory(BaseRecipeFactory)
    quantity = fuzzy.FuzzyInteger(50, 500)

    class Meta:
        model = models.RecipeIngredient

    @factory.lazy_attribute
    def ingredient(self):
        return choice(models.Ingredient.objects.all())


class RecipeFactory(BaseRecipeFactory):
    """Factory that generates Recipes with random amount of Ingredients."""

    ingredients_amount = randint(1, 7)

    for _ in ingredients_amount:
        ingredient = factory.RelatedFactory(
            RecipeIngredientFactory,
            factory_related_name='recipe',
        )

    # ingredient_1 = factory.RelatedFactory(
    #     RecipeIngredientFactory,
    #     factory_related_name='recipe',
    # )
    # ingredient_2 = factory.RelatedFactory(
    #     RecipeIngredientFactory,
    #     factory_related_name='recipe',
    # )
    # ingredient_3 = factory.RelatedFactory(
    #     RecipeIngredientFactory,
    #     factory_related_name='recipe',
    # )
    # ingredient_4 = factory.RelatedFactory(
    #     RecipeIngredientFactory,
    #     factory_related_name='recipe',
    # )
    # ingredient_5 = factory.RelatedFactory(
    #     RecipeIngredientFactory,
    #     factory_related_name='recipe',
    # )
