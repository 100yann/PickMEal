from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('register', views.register, name='register'),
    path('login', views.log_in, name='login'),
    path('logout', views.log_out, name='logout'),
    path('recipe/<int:recipe_id>', views.recipe, name='recipe'),
    path('results', views.results, name='recipe_results')
]