from django import forms
from django.forms import CheckboxSelectMultiple

from .models import Recipe, Ingredient


class RecipeForm(forms.ModelForm):
	class Meta:
		model = Recipe
		fields = ("title", "description", "cooking_time", "ingredient", "image", "tag")
		widgets = {
			'tag': CheckboxSelectMultiple(),
		}
		labels = {
			'title': "Название рецепта",
			'tag': "Теги",
			'ingredient': "Ингредиенты",
			'cooking_time': "Время приготовления",
			'description': "Описание",
			'image': "Загрузить фото",
		}
		help_texts = {
			'title': "Укажите название рецепта:",
			'description': "Опишите Ваш рецепт:",
			'cooking_time': "Укажите время приготовления",
			'ingredient': "Выберите ингредиенты",
			'image': "Загрузите Ваше изображение (если, конечно, хотите):",
			'tag': "Выберите релевантные тэги",
		}

	ingredient = forms.ModelMultipleChoiceField(
		queryset=Ingredient.objects.all()
	)

	def clean_recipe(self):
		data = self.cleaned_data("title", "description", )
		if not data:
			raise forms.ValidationError("Ваш рецепт неполон")

		return data
