from django.shortcuts import render
from .models import Dish

def home(request):
    dishes = Dish.objects.all()
    return render(request, 'home.html', {'dishes': dishes})