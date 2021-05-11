from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Tag(models.Model):
	name = models.CharField(max_length=125)
	slug = models.SlugField(unique=True)

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


class Recipe(models.Model):
	title = models.CharField(max_length=250, verbose_name='Название')
	slug = models.SlugField(unique=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
	description = models.TextField(verbose_name='Описание')
	cooking_time = models.PositiveIntegerField(verbose_name='Время приготовления')
	ingredient = models.ManyToManyField(Ingredient, through='RecipeIngredient', verbose_name='Ингредиенты')
	image = models.ImageField(upload_to='recipes/images/', null=True, blank=True, verbose_name='Изображение')
	tag = models.ManyToManyField(Tag, db_constraint=True, verbose_name='Тэги')
	pub_date = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата публикации')

	class Meta:
		verbose_name = 'Рецепт'
		verbose_name_plural = 'Рецепты'
		ordering = ('-pub_date',)

	def __str__(self):
		return self.title


class RecipeIngredient(models.Model):
	recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name='Рецепт')
	ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, verbose_name='Ингредиент')
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
		related_name='shopping_cart',
		verbose_name='Пользователь'
	)
	recipe = models.ForeignKey(
		Recipe,
		on_delete=models.CASCADE,
		related_name='shopping_cart',
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
