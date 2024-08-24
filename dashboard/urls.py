from django.urls import path
from . import views
urlpatterns = [
    #dashboard
    path('stats/', views.stats_view, name='stats'),
    path('order/<int:order_id>/', views.order_detail_view, name='order_detail'),

    path('messages/', views.message_list, name='message_list'),
    path('messages/<int:pk>/', views.message_detail, name='message_detail'),

    path('users/', views.user_list_view, name='user_list'),
    path('export-users/', views.export_users_to_excel, name='export_users_to_excel'),

    path('subscribers/', views.subscriber_list, name='subscriber_list'),
    path('subscribers/export/', views.export_subscribers_to_excel, name='export_subscribers'),

    path('manage-orders/', views.manage_orders, name='manage_orders'),
]
