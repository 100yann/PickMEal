from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name='home'),
    path('register', views.register, name='register'),
    path('login', views.log_in, name='login'),
    path('logout', views.log_out, name='logout'),
    path('recipe/<int:recipe_id>', views.recipe, name='recipe'),
    path('results', views.results, name='recipe_results'),
    path('create', views.new_recipe, name='new_recipe'),
    path('user/<int:id>', views.user, name='user')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)