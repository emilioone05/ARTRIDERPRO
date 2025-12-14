from django.db import models
from django.conf import settings # Para referenciar al usuario

class Categoria(models.Model):
    nombre = models.CharField(max_length=100) # Sonido, Luces, Video

    def __str__(self):
        return self.nombre

class Equipo(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    foto_principal = models.URLField(blank=True, null=True) 
    propietario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mis_equipos')
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

class FotoEquipo(models.Model):
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='fotos')
    url_imagen = models.URLField()

class Inventario(models.Model):
    equipo = models.OneToOneField(Equipo, on_delete=models.CASCADE, related_name='inventario')
    precio_por_dia = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad_total = models.PositiveIntegerField(default=1) # Stock total físico

    def __str__(self):
        return f"Inventario de {self.equipo.titulo}"