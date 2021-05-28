from django.core.management.base import BaseCommand
from recipes.models import Tag

TAGS = (
    {
        'name': 'Завтрак',
        'slug': 'breakfast',
        'color': 'orange',
    },
    {
        'name': 'Обед',
        'slug': 'lunch',
        'color': 'green',
    },
    {
        'name': 'Ужин',
        'slug': 'dinner',
        'color': 'purple',
    },
)

class Command(BaseCommand):
	help = 'Pre-fill initial tags'

	def handle(self, *args, **options):

            self.tags = TAGS
            for item in self.tags:
                Tag.objects.get_or_create(name=item['name'], slug=item['slug'], color=item['color'])
