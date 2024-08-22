from decimal import Decimal
from django.shortcuts import get_object_or_404, redirect, render
from cart.models import Cart
from categories.models import Product
from orders.models import Order
import stripe
from django.conf import settings
from django.http import JsonResponse

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
        products = []
        product_ids = request.POST.getlist('products[id]')
        quantities = request.POST.getlist('products[quantity]')
        for product_id, quantity in zip(product_ids, quantities):
            products.append({'product_id': product_id, 'quantity': quantity})
        total_amount = int(float(request.POST.get('total')) * 100)
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
        if payment_method == 'bank_transfer':
            return redirect(f'/order/create-checkout-session/{order.id}/{total_amount}/')
        return redirect('index')
    return render(request, 'orders/checkout.html')

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

def create_checkout_session(request, order_id , amount):
    if request.method == 'GET':
        YOUR_DOMAIN = "http://localhost:8000" 
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': 'Sample Product',
                        },
                        'unit_amount': int(amount),
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=f'{YOUR_DOMAIN}/order/success/{order_id}',
            cancel_url=f'{YOUR_DOMAIN}/order/cancel/',
        )
        return redirect(checkout_session.url, code=303)

    return JsonResponse({"error": "Invalid request"}, status=400)

def success_view(request,order_id):

    if order_id:
        try:
            order = get_object_or_404(Order, id=order_id)
            order.is_paid = 'True'
            order.save()
        except Order.DoesNotExist:
            print(f"Order with ID {order_id} does not exist")
    return render(request, 'orders/success.html')


def cancel_view(request):
    return render(request, 'orders/cancel.html')
