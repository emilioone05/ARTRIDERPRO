from django.contrib import admin
from .models import Reserva, ReservaItem

# Esto permite ver los items (equipos/paquetes) DENTRO de la reserva
class ReservaItemInline(admin.TabularInline):
    model = ReservaItem
    extra = 0 # Para que no muestre filas vacías extra

class ReservaAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'propietario', 'fecha_inicio', 'fecha_fin', 'estado', 'precio_total')
    list_filter = ('estado', 'fecha_inicio') # Filtros laterales útiles
    search_fields = ('cliente__email', 'cliente__username') # Barra de búsqueda
    inlines = [ReservaItemInline] # <--- Aquí conectamos los items

admin.site.register(Reserva, ReservaAdmin)
# No registramos ReservaItem por separado porque ya se ve dentro de Reserva