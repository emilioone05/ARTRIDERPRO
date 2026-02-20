from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Heredamos de UserAdmin para mantener la funcionalidad de contraseñas de Django
class CustomUserAdmin(UserAdmin):
    # 1. COLUMNAS DE LA TABLA (Lo que ves en la lista)
    list_display = (
        'email', 
        'username', 
        'phone', 
        'role', 
        'city', 
        'is_verified', 
        'is_staff'
    )
    
    # 2. FILTROS LATERALES (Barra derecha para filtrar rápido)
    list_filter = ('role', 'is_verified', 'city', 'is_staff')

    # 3. SECCIONES DEL FORMULARIO DE EDICIÓN
    # UserAdmin.fieldsets trae los campos por defecto (pass, user, dates...)
    # Nosotros le sumamos ('+') nuestra sección personalizada.
    fieldsets = UserAdmin.fieldsets + (
        ('Información Extra ArtRider', {
            'fields': ('phone', 'role', 'city', 'avatar', 'is_verified')
        }),
    )

    # Configuración adicional para búsquedas
    search_fields = ('email', 'username', 'phone', 'city')
    ordering = ('email',)

# Registramos el modelo con nuestra configuración
admin.site.register(User, CustomUserAdmin)