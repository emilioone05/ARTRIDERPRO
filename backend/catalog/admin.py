from django.contrib import admin
from .models import Categoria, Equipo, Inventario, FotoEquipo

class InventarioInline(admin.StackedInline):
    model = Inventario

class EquipoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'propietario', 'created_at')
    # Esto permite editar el inventario DENTRO de la pantalla de Equipo
    inlines = [InventarioInline]

admin.site.register(Categoria)
admin.site.register(Equipo, EquipoAdmin)
admin.site.register(Inventario)
admin.site.register(FotoEquipo)