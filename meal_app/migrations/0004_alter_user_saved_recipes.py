# Generated by Django 4.2.5 on 2023-11-04 15:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("meal_app", "0003_user_saved_recipes"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="saved_recipes",
            field=models.JSONField(default=list),
        ),
    ]