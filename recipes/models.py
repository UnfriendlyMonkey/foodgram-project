from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Tag(models.Model):
	name = models.CharField(max_length=125)
	slug = models.SlugField(unique=True)

	def __str__(self):
		return self.name


class Ingredient(models.Model):
	name = models.CharField(max_length=250)
	unit = models.CharField(max_length=125)

	def __str__(self):
		return f"{self.name}, {self.unit}"


class Recipe(models.Model):
	title = models.CharField(max_length=250)
	slug = models.SlugField(unique=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	description = models.TextField()
	cooking_time = models.PositiveIntegerField()
	ingredient = models.ManyToManyField(Ingredient, through='RecipeIngredient')
	image = models.ImageField(upload_to='images/', null=True, blank=True)
	tag = models.ManyToManyField(Tag, db_constraint=True)

	def __str__(self):
		return self.title


class RecipeIngredient(models.Model):
	recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
	ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField()


class Follow(models.Model):
	follower = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='follower'
	)
	following = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='following'
	)

	class Meta:
		constraints = [
			models.UniqueConstraint(
				fields=('follower', 'following'),
				name='unique_follow'
			),
		]

	def __str__(self):
		return f"{self.follower} following {self.following}"
