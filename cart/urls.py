from django.urls import path
from . import views

urlpatterns = [
    path('add-to-cart/<int:product_id>/<int:quantity>/', views.add_to_cart, name='add_to_cart'),
    path('', views.view_cart, name='view_cart'),
    path('remove-from-cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
]
