# Generated by Django 3.2.2 on 2021-05-20 05:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0011_alter_recipe_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shoppingcart',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='in_cart', to='recipes.recipe', verbose_name='Рецепт для покупки'),
        ),
        migrations.AlterField(
            model_name='shoppingcart',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchases', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]