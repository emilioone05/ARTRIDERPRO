from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Rol

# Esto permite que Django sepa cómo manejar contraseñas en tu usuario personalizado
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # Estos son los campos que se verán en la lista de usuarios
    list_display = ['email', 'username', 'rol', 'is_staff', 'is_active']
    
    # Esto es importante para que puedas editar tus campos personalizados en el admin
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('rol', 'phone_number', 'company_name', 'location', 'description')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('rol', 'phone_number', 'company_name', 'location', 'description')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Rol)