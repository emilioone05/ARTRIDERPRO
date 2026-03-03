
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView, 
    SpectacularSwaggerView, 
    SpectacularRedocView
)
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
    # --- SWAGGER Y SCHEMA ---
    
    # 1. Generación del Archivo de Esquema (descarga el YAML)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    # 2. Interfaz Swagger UI (La que buscas)
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # 3. Interfaz Redoc (Opcional, otra forma de ver la doc)
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)