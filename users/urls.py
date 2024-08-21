from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('product/', views.product, name='product'),
    path('contact/', views.contact, name='contact'),
    path('shop/', views.shop, name='shop'),   
    path('login/', views.login, name='login'), 
]
