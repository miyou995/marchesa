from django.shortcuts import render , get_object_or_404
from .models import Category

def category(request):
    categories = Category.objects.filter(actif=True)
    return {
            'categories' : categories
        }
    

