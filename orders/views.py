from decimal import Decimal
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from cart.models import Cart

def checkout_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    for item in cart_items:
        product = item.product
        if product.is_on_sale:
            item_price = product.sale_price
        else:
            item_price = product.price
        item.total_price = Decimal(item_price) * item.quantity
    subtotal = sum(item.total_price for item in cart_items)
    shipping_cost = Decimal('5.00')
    total = subtotal + shipping_cost
    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping_cost': shipping_cost,
        'total': total
    }
    return render(request, 'orders/checkout.html', context)