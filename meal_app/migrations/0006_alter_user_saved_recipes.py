# Generated by Django 4.2.5 on 2023-11-04 15:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("meal_app", "0005_alter_user_saved_recipes"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="saved_recipes",
            field=models.JSONField(blank=True, default=list, null=True),
        ),
    ]
