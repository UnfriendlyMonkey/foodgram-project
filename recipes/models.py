from django.db import models


class Ingredient(models.Model):
	name = models.CharField(max_length=250)
	unit = models.CharField(max_length=125)

	def __str__(self):
		return f"{self.name}, {self.unit}"
