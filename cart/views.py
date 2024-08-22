from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Cart
from categories.models import Product


@login_required(login_url='/login/')
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
    out_of_stock_items = []
    for item in cart_items:
        product = item.product
        if product.is_on_sale:
            item_price = product.sale_price
        else:
            item_price = product.price
        item.product.price = item_price
        if product.is_in_stock <= 0:
            out_of_stock_items.append(item.id)
    if out_of_stock_items:
        Cart.objects.filter(id__in=out_of_stock_items).delete()
    return render(request, 'cart/cart.html', {'cart_items': cart_items})


def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)
    cart_item.delete()
    return redirect('view_cart')

def clear_cart(request):
    Cart.objects.filter(user=request.user).delete()
    return redirect('view_cart')


def get_cart_count(request):
    if request.user.is_authenticated:
        count = Cart.objects.filter(user=request.user).count()
    else:
        count = 0
    return JsonResponse({'count': count})