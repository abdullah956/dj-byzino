from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout_view, name='checkout'),
    path('checkout-process/', views.checkout_process_view, name='checkout_process'),


    path('create-checkout-session/<int:amount>/', views.create_checkout_session, name='create_checkout_session'),
    path('success/', views.success_view, name='success'),
    path('cancel/', views.cancel_view, name='cancel'),
]
