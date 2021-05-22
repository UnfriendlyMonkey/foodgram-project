from django import forms
# from django.forms import CheckboxSelectMultiple

from .models import Recipe, Ingredient


class RecipeForm(forms.ModelForm):
	class Meta:
		model = Recipe

		fields = ("title", "description", "cooking_time", "image")

		image = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form__file'}))

	def clean_recipe(self):
		data = self.cleaned_data("title", "description", )
		if not data:
			raise forms.ValidationError("Ваш рецепт неполон")

		return data
