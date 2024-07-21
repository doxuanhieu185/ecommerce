from django.shortcuts import render
from . models import Category, Products

from django.shortcuts import get_object_or_404
# Create your views here.


def store(request):
    
    all_product = Products.objects.all()
    context = {'my_products': all_product}
    
    return render(request, 'store/store.html', context)


def categories(request):
    all_categories = Category.objects.all()
    
    return {'all_categories': all_categories}

def list_category(request, category_slug:None):
    category = get_object_or_404(Category, slug = category_slug)
    products = Products.objects.filter(category=category)
    return render(request, 'store/list-category.html', {'category':category, 'products':products})

def product_infor(request, product_slug):
    product = get_object_or_404(Products, slug = product_slug )
    context = {'product': product}
    
    return render(request, 'store/product-info.html', context)