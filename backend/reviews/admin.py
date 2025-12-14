from django.contrib import admin
from .models import Review

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'autor', 'reserva', 'calificacion', 'created_at')
    list_filter = ('calificacion',) # Filtrar por estrellas (1 a 5)
    search_fields = ('comentario', 'autor__username')

admin.site.register(Review, ReviewAdmin)