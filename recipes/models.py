from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Ingredient(models.Model):
	name = models.CharField(max_length=250)
	unit = models.CharField(max_length=125)

	def __str__(self):
		return f"{self.name}, {self.unit}"


class Recipe(models.Model):
	title = models.CharField(max_length=250)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	description = models.TextField()
	cooking_time = models.PositiveIntegerField()
	ingredient = models.ManyToManyField(Ingredient, through='RecipeIngredient')

	def __str__(self):
		return self.title


class RecipeIngredient(models.Model):
	recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
	ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField()
