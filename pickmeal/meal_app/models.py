from django.db import models
from django.contrib.auth.models import AbstractUser
from django import forms
import json 
# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    saved_recipes = models.ManyToManyField('Recipe', related_name='users_who_saved')

    
    def get_recipes(self):
        return self.saved_recipes

    def __str__(self) -> str:
        return self.username
    

class Recipe(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    ingredients = models.TextField(blank=True)
    instructions = models.TextField(blank=True, null=True)
    description = models.CharField(blank=True, max_length=10000)
    servings = models.SmallIntegerField(blank=True)
    image = models.URLField(blank=True)

class UserRecipes(models.Model):
    title = models.CharField(max_length=255)
    ingredients = models.TextField()
    instructions = models.TextField()
    description = models.CharField(max_length=10000)
    servings = models.SmallIntegerField()

class Rating(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ratings')
    rating = models.IntegerField()
    rated_by = models.ForeignKey(User, on_delete=models.CASCADE)


class RegisterUser(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        
        self.fields['email'].required = True


