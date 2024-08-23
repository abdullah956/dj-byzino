from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    #auth
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    #email verfication 
    path('send-otp/', views.send_otp_view, name='send_otp'),
    path('verify-otp/', views.verify_otp_view, name='verify_otp'),
    #password reset
    path('forgot_password/', views.forgot_password_view, name='forgot_password'),
    path('send-password-otp/', views.send_password_otp_view, name='send_password_otp'),
    path('verify_password_otp/', views.verify_password_otp_view, name='verify_password_otp'),
    path('reset_password/', views.reset_password_view, name='reset_password'),
    #logout
    path('logout/', views.logout_view, name='logout'),
    #profile update
    path('profile/update/', views.update_profile_view, name='update_profile'),
    #subs
    path('subscribe/', views.subscribe_view, name='subscribe'),
    #contact
    path('contact/', views.contact_view, name='contact'),
    path('contact/message', views.contact_message_view, name='contact_message'),
    #search
    path('search/', views.product_search_view, name='product_search'),
    #dashboard
    path('stats/', views.stats_view, name='stats'),
    path('dashboard/order/<int:order_id>/', views.order_detail_view, name='order_detail'),

    path('messages/', views.message_list, name='message_list'),
    path('messages/<int:pk>/', views.message_detail, name='message_detail'),

    path('users/', views.user_list_view, name='user_list'),
    path('export-users/', views.export_users_to_excel, name='export_users_to_excel'),
]
