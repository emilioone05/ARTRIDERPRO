from django.contrib import admin
from .models import CustomUser, Rol, Categoria, Equipo, FotoEquipo, Inventario, Paquete, PaqueteItem, Reserva, ReservaItem, Review

admin.site.register(CustomUser)
admin.site.register(Rol)
admin.site.register(Categoria)
admin.site.register(Equipo)
admin.site.register(FotoEquipo)
admin.site.register(Inventario)
admin.site.register(Paquete)
admin.site.register(PaqueteItem)
admin.site.register(Reserva)
admin.site.register(ReservaItem)
admin.site.register(Review)