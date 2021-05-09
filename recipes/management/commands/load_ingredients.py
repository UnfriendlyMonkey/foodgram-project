from django.core.management.base import BaseCommand
from recipes.models import Ingredient
import csv
import os
from foodgram.settings import BASE_DIR

CSV_FILE_PATH = os.path.join(BASE_DIR, 'ingredients.csv')


class Command(BaseCommand):
	help = 'Load ingredients'

	def handle(self, *args, **options):
		with open(CSV_FILE_PATH) as file:
			reader = csv.reader(file)
			for row in reader:
				name, unit = row
				Ingredient.objects.get_or_create(name=name, unit=unit)
