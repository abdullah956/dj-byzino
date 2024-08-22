from decimal import Decimal
import json
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from cart.models import Cart
from categories.models import Product
from orders.models import Order

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



def checkout_process_view(request):
    if request.method == 'POST':
        # Extract form data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')
        billing_address = request.POST.get('billing_address')
        shipping_address = request.POST.get('shipping_address')
        postal_code = request.POST.get('postal_code')
        phone = request.POST.get('phone')
        payment_method = request.POST.get('payment_method')

        # Extract product data
        products = []
        product_ids = request.POST.getlist('products[id]')
        quantities = request.POST.getlist('products[quantity]')
        for product_id, quantity in zip(product_ids, quantities):
            products.append({'product_id': product_id, 'quantity': quantity})

        total_amount = request.POST.get('total')

        order = Order.objects.create(
            user=request.user,
            first_name=first_name,
            last_name=last_name,
            email=email,
            country=country,
            state=state,
            city=city,
            billing_address=billing_address,
            shipping_address=shipping_address,
            postal_code=postal_code,
            phone=phone,
            payment_method=payment_method,
            amount=total_amount,
            is_shipped=False,
            status='placed',
            products=products
        )
        order.save()
        # Clear the cart if needed
        # Cart.objects.filter(user=request.user).delete()

        return redirect('index')  # Redirect to a success page or similar

    return render(request, 'orders/checkout.html')