from django.shortcuts import render

from categories.models import Category, Product


def products_view(request):
    products = Product.objects.all()
    return render(request, 'categories/shop.html', {'products': products})