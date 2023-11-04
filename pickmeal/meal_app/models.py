from django.db import models
from django.contrib.auth.models import AbstractUser
from django import forms
import json 
# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    saved_recipes = models.JSONField(default=list, blank=True)

    def add_recipe(self, recipe_id):
        self.saved_recipes.append(recipe_id)
        self.save()

    def remove_recipe(self, recipe_id):
        if recipe_id in self.saved_recipes:
            self.saved_recipes.remove(recipe_id)
            self.save()
    
    def get_recipes(self):
        return self.saved_recipes

    def __str__(self) -> str:
        return f'Username: {self.username}\nSaved recipes: {self.saved_recipes}'
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


