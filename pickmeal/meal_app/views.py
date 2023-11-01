from django.shortcuts import render
from django.conf import settings

# Create your views here.
def index(request):
    context = {
        'SPOONACULAR_API_KEY': settings.SPOONACULAR_API_KEY
    }

    return render(request, 'index.html', context)