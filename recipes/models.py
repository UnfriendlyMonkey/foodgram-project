from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Exists, OuterRef, Case, When
from typing import Optional


User = get_user_model()


class Tag(models.Model):
	name = models.CharField(max_length=125)
	slug = models.SlugField(unique=True)
	color = models.CharField(max_length=50)

	def __str__(self):
		return self.name


class Ingredient(models.Model):
	name = models.CharField(max_length=250, verbose_name='Название')
	unit = models.CharField(max_length=125, verbose_name='Единица измерения')

	class Meta:
		verbose_name = 'Ингредиент'
		verbose_name_plural = 'Ингредиенты'
		ordering = ('name',)

	def __str__(self):
		return f"{self.name}, {self.unit}"


class RecipeQuerySet(models.QuerySet):
	def with_favorite_and_cart(self, user_id: Optional[int]):
		"""Annotate with favorite flag."""
		return self.annotate(is_favorite=Exists(
			Favorite.objects.filter(
				user_id=user_id,
				recipe_id=OuterRef('pk'),
			),
		)).annotate(is_in_cart=Exists(
			ShoppingCart.objects.filter(
				user_id=user_id,
				recipe_id=OuterRef('pk')
			),
		))

	def with_session_data(self, in_cart):
		return self.annotate(is_in_cart=Case(When(id__in=in_cart, then=True)))


class Recipe(models.Model):
	title = models.CharField(max_length=250, verbose_name='Название')
	user = models.ForeignKey(User, related_name='recipes', on_delete=models.CASCADE, verbose_name='Автор')
	description = models.TextField(verbose_name='Описание')
	cooking_time = models.PositiveIntegerField(verbose_name='Время приготовления')
	ingredient = models.ManyToManyField(Ingredient, through='RecipeIngredient', verbose_name='Ингредиенты')
	image = models.ImageField(upload_to='recipes/images/', null=True, verbose_name='Изображение')
	tag = models.ManyToManyField(Tag, related_name='recipes', db_constraint=True, verbose_name='Тэги')
	pub_date = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата публикации')

	objects = RecipeQuerySet.as_manager()

	class Meta:
		verbose_name = 'Рецепт'
		verbose_name_plural = 'Рецепты'
		ordering = ('-pub_date',)

	def __str__(self):
		return self.title


class RecipeIngredient(models.Model):
	recipe = models.ForeignKey(
		Recipe,
		on_delete=models.CASCADE,
		verbose_name='Рецепт',
		related_name='recipe_ingredients',
	)
	ingredient = models.ForeignKey(
		Ingredient,
		on_delete=models.CASCADE,
		verbose_name='Ингредиент',
		related_name='ingredient_recipes'
	)
	quantity = models.PositiveIntegerField(verbose_name='Количество')


class Follow(models.Model):
	follower = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='follower',
		verbose_name='Подписчик'
	)
	following = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='following',
		verbose_name='Подписка'
	)

	class Meta:
		constraints = [
			models.UniqueConstraint(
				fields=('follower', 'following'),
				name='unique_follow'
			),
		]

	def __str__(self):
		return f"{self.follower} подписан(а) на {self.following}"


class Favorite(models.Model):
	user = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='favorites',
		verbose_name='Пользователь'
	)
	recipe = models.ForeignKey(
		Recipe,
		on_delete=models.CASCADE,
		related_name='favorites',
		verbose_name='Любимый рецепт'
	)

	def __str__(self):
		return f'{self.user} добавил {self.recipe} в избранное'

	class Meta:
		constraints = [
			models.UniqueConstraint(
				fields=('user', 'recipe'),
				name='unique_favorite'
			),
		]


class ShoppingCart(models.Model):
	user = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='purchases',
		verbose_name='Пользователь'
	)
	recipe = models.ForeignKey(
		Recipe,
		on_delete=models.CASCADE,
		related_name='in_cart',
		verbose_name='Рецепт для покупки'
	)

	def __str__(self):
		return f'{self.user} добавил {self.recipe} в список покупок'

	class Meta:
		constraints = [
			models.UniqueConstraint(
				fields=('user', 'recipe'),
				name='unique_shopping_cart'
			),
		]
