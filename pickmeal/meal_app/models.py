from django.db import models
from django.contrib.auth.models import AbstractUser
from django import forms
from django.db.models import Avg


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
    added_on = models.DateField(auto_now=True)

    @classmethod
    def getRecentRecipes(cls, num):
        return cls.objects.all().order_by('-added_on')[:num]
    
    @classmethod
    def getTopRecipes(cls, num):
        return cls.objects.annotate(avg_rating=Avg('ratings__rating')).order_by('-avg_rating')[:num]



def upload_location(instance, filename):
    file, extension = filename.split('.')
    return 'recipe_images/%s.%s' % (instance.title, extension)

class UserRecipes(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    ingredients = models.TextField()
    instructions = models.TextField()
    description = models.CharField(max_length=10000)
    servings = models.SmallIntegerField()
    image = models.ImageField(upload_to=upload_location)
    cooking_time = models.SmallIntegerField()

    def __str__(self) -> str:
        output = ''
        for var in vars(self).values():
            output += str(var) + '\n'
        return output

class Rating(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ratings')
    rating = models.IntegerField()
    rated_by = models.ForeignKey(User, on_delete=models.CASCADE)


# Model Forms
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


class NewUserRecipe(forms.ModelForm):
    class Meta:
        model = UserRecipes
        fields = ['title', 'description', 'image', 'servings', 'cooking_time']
        widgets={
                "title":forms.TextInput(attrs={'placeholder':'','name':'recipe-title','class':'form-control new-recipe'}),
                "description":forms.Textarea(attrs={'placeholder':'','name':'recipe-description','class':'form-control new-recipe'}),
                "servings": forms.NumberInput(attrs={'placeholder': '', 'class': 'form-control'}),
                "cooking_time": forms.NumberInput(attrs={'placeholder': '', 'class': 'form-control'}),
            }  


