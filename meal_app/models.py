from django.db import models
from django.contrib.auth.models import AbstractUser
from django import forms
from django.db.models import Avg
from PIL import Image

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    saved_recipes = models.ManyToManyField('Recipe', related_name='users_who_saved')
    
    def get_recipes(self):
        return self.saved_recipes

    def __str__(self) -> str:
        return self.username
    

def upload_location(instance, filename):
    file, extension = filename.split('.')
    return 'recipe_images/%s.%s' % (instance.recipe.title, extension)


class Recipe(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    spoonacular_id = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=75)
    added_on = models.DateTimeField(auto_now=True)

    @classmethod
    def getRecentRecipes(cls, num):
        return cls.objects.all().order_by('-added_on')[:num]
    
    @classmethod
    def getTopRecipes(cls, num):
        return cls.objects.annotate(avg_rating=Avg('ratings__rating')).order_by('-avg_rating')[:num]

    def calculate_average_rating(self):
        return self.ratings.aggregate(Avg('rating'))['rating__avg']


class RecipeDetails(models.Model):
    recipe = models.OneToOneField(Recipe, on_delete=models.CASCADE)
    ingredients = models.TextField(blank=True)
    instructions = models.TextField(blank=True, null=True)
    description = models.CharField(blank=True, max_length=10000)
    cooking_time = models.SmallIntegerField()
    servings = models.SmallIntegerField(blank=True)
    image = models.URLField(blank=True, null=True)
    upload_image = models.ImageField(upload_to=upload_location, blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.upload_image:
            img = Image.open(self.upload_image.path)
            output_size = (556, 370)
            img.thumbnail(output_size)
            img.save(self.upload_image.path)

    def ingredients_to_list(self):
        replacements = {"[": "{", "]":"}", '"': "'", "{'": "", "'}": ""}
        cleaned_string = self.ingredients
        for old, new in replacements.items():
            cleaned_string = cleaned_string.replace(old, new)
        if self.recipe.created_by:
            return cleaned_string.split(", ")
        else:
            return cleaned_string.split("', '")
    
    def instructions_to_list(self):
        cleaned_instructions = self.instructions.replace("['", '').replace("']", '')
        return cleaned_instructions.split("', '")


class RecipeDietaryTags(models.Model):
    recipe = models.OneToOneField(Recipe, on_delete=models.CASCADE)
    vegetarian = models.BooleanField(null=True)
    vegan = models.BooleanField(null=True)
    dairy_free = models.BooleanField(null=True)
    gluten_free = models.BooleanField(null=True)

    def check_tags(self):

        tags = []
        for field_name in self._meta.get_fields():
            if field_name.name not in ['recipe', 'id'] and getattr(self, field_name.name):
                tags.append(field_name.name.title().replace('_', ' '))

        return tags
    
    def check_matching_tags(self, dietary_tags):
        fields = {
            'vegan': self.vegan, 
            'vegetarian': self.vegetarian,
            'dairy_free': self.dairy_free,
            'gluten_free': self.gluten_free
            }
        for tag in dietary_tags:
            if fields.get(tag, False):
                continue
            else:
                return False
        return True
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
        self.fields['password'].helptext = ''


class NewRecipe(forms.ModelForm):

    class Meta:
        model = RecipeDetails
        fields = ['servings', 'cooking_time', 'description', 'upload_image']
        widgets={
                'cooking_time': forms.NumberInput(attrs={'class': 'form-control'}),
                'servings': forms.NumberInput(attrs={'class': 'form-control'}),
                'description': forms.Textarea(attrs={'placeholder': '', 'class': 'form-control new-recipe'})
            }  


