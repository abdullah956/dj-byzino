from django.shortcuts import get_object_or_404, render

from categories.models import Category, Product


def products_view(request):
    products = Product.objects.all()
    return render(request, 'categories/shop.html', {'products': products})

def product_detail_view(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'categories/product_detail.html', {'product': product})

def category_products_view(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    return render(request, 'categories/category_products.html', {'category': category, 'products': products})