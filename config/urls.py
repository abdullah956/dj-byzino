from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from config import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('category/', include('categories.urls')),
    path('cart/', include('cart.urls')), 
    path('order/', include('orders.urls')), 
    path('dashboard/', include('dashboard.urls')), 
    path('blogs/', include('blogs.urls')), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
