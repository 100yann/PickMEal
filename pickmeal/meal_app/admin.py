from django.contrib import admin
from .models import User, Rating, Recipe
# Register your models here.

admin.site.register(User)
admin.site.register(Rating)
admin.site.register(Recipe)