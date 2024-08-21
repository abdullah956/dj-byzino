from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.products_view, name='products'),
    path('product/<int:id>/', views.product_detail_view, name='product_detail'),
]


