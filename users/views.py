from django.shortcuts import render

def home(request):
    return render(request, 'home.html')



def cart(request):
    return render(request, 'cart.html')


def contact(request):
    return render(request, 'contact.html')


def product(request):
    return render(request, 'product.html')


def shop(request):
    return render(request, 'shop.html')



def checkout(request):
    return render(request, 'checkout.html')

def login(request):
    return render(request, 'login.html')