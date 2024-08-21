from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Cart
from categories.models import Product

def add_to_cart(request, product_id, quantity):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(quantity)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
    cart_item.save()
    return redirect('view_cart')

def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    for item in cart_items:
        product = item.product
        if product.is_on_sale:
            product.price = product.sale_price

        else:
            product.price = product.price
    
    return render(request, 'cart/cart.html', {'cart_items': cart_items})


def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)
    cart_item.delete()
    return redirect('view_cart')

def clear_cart(request):
    Cart.objects.filter(user=request.user).delete()
    return redirect('view_cart')