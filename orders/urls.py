from django.urls import path
from .views import checkout_view , checkout_process_view

urlpatterns = [
    path('checkout/', checkout_view, name='checkout'),
    path('checkout-process/', checkout_process_view, name='checkout_process'),
]
