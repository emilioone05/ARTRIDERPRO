# """
# URL configuration for config project.

# The `urlpatterns` list routes URLs to views. For more information please see:
#     https://docs.djangoproject.com/en/6.0/topics/http/urls/
# Examples:
# Function views
#     1. Add an import:  from my_app import views
#     2. Add a URL to urlpatterns:  path('', views.home, name='home')
# Class-based views
#     1. Add an import:  from other_app.views import Home
#     2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
# Including another URLconf
#     1. Import the include() function: from django.urls import include, path
#     2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
# """
# from django.conf import settings             # <--- Importar
# from django.conf.urls.static import static   #
# from django.contrib import admin
# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from inventory.views import PublicationViewSet, UnitViewSet, PackageViewSet, CategoryViewSet    
# from bookings.views import ReservationViewSet
# from users.views import UserViewSet

# router = DefaultRouter()
# router.register(r'publicaciones', PublicationViewSet)
# router.register(r'unidades', UnitViewSet)
# router.register(r'reservas', ReservationViewSet)
# router.register(r'paquetes', PackageViewSet)
# router.register(r'users', UserViewSet)
# router.register(r'categories', CategoryViewSet)

# urlpatterns = [
#     path('admin/', admin.site.urls),
    
#     path('api/', include(router.urls)), # Todas las APIs estarán en /api/
#     path('api/inventory/', include('inventory.urls')), 
    
#     # ... tus otras rutas (users, bookings, etc)
#     path('api/users/', include('users.urls')), 
    
#     # path('api/users/', include('users.urls')),
#     path('api/', include('bookings.urls')),
# ]
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# backend/config/urls.py (o el nombre de tu carpeta principal)
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # 1. USUARIOS -> /api/users/
    path('api/', include('users.urls')),

    # 2. RESERVAS -> /api/bookings/
    # Esto soluciona tu 404 si el front llama a /api/bookings/
    path('api/', include('bookings.urls')),

    # 3. INVENTARIO -> /api/publicaciones/ y /api/categories/
    # Al usar 'api/', tus llamadas en provider.service funcionarán directo
    path('api/', include('inventory.urls')), 
    
    # 4. EXCEPCIÓN: Rutas personalizadas del Proveedor
    # Como en tu servicio tienes hardcoded 'api/inventory/provider/...',
    # agregamos esta línea para que esas URLs específicas no se rompan.
    path('api/inventory/', include('inventory.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)