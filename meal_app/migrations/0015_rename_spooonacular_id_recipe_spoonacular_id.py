# Generated by Django 4.2.6 on 2023-11-17 17:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meal_app', '0014_remove_recipe_cooking_time_remove_recipe_description_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='spooonacular_id',
            new_name='spoonacular_id',
        ),
    ]