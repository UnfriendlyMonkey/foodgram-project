from django import forms
# from django.forms import CheckboxSelectMultiple

from .models import Recipe, Ingredient, Tag


class RecipeForm(forms.ModelForm):
	class Meta:
		model = Recipe

		fields = ("title", "description", "cooking_time", "image")

		image = forms.FileField(
			widget=forms.ClearableFileInput(attrs={'class': 'form__file'}),
			required=True)

	def clean(self):

		cleaned_data = super().clean()
		print(cleaned_data)

		tags = [item[0] for item in Tag.objects.values_list('slug')]

		error_tag = True
		error_ingredient = True

		for key in self.data.keys():
			if 'nameIngredient' in key:
				error_ingredient = False
			if key in tags:
				error_tag = False

		if error_tag:
			raise forms.ValidationError('Добавьте хотя бы один тег')

		if error_ingredient:
			raise forms.ValidationError('Добавьте ингредиенты')

		data = ("title", "description", "cooking_time", "image")
		for item in data:
			if not cleaned_data[item]:
				raise forms.ValidationError("Ваш рецепт неполон")

		return cleaned_data
