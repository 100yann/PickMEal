# Generated by Django 4.2.6 on 2023-11-17 17:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import meal_app.models


class Migration(migrations.Migration):

    dependencies = [
        ('meal_app', '0013_recipe_cooking_time_recipe_created_by_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='cooking_time',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='description',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='ingredients',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='instructions',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='servings',
        ),
        migrations.AddField(
            model_name='recipe',
            name='spooonacular_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='upload_image',
            field=models.ImageField(blank=True, null=True, upload_to=meal_app.models.upload_location),
        ),
        migrations.CreateModel(
            name='RecipeDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ingredients', models.TextField(blank=True)),
                ('instructions', models.TextField(blank=True, null=True)),
                ('description', models.CharField(blank=True, max_length=10000)),
                ('cooking_time', models.SmallIntegerField()),
                ('servings', models.SmallIntegerField(blank=True)),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meal_app.recipe')),
            ],
        ),
    ]
