from django.contrib import admin
from .models import Paquete, PaqueteItem

class PaqueteItemInline(admin.TabularInline):
    model = PaqueteItem

class PaqueteAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'propietario', 'precio_por_dia')
    inlines = [PaqueteItemInline]

admin.site.register(Paquete, PaqueteAdmin)