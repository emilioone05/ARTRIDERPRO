from django.db import models
from django.conf import settings
from catalog.models import Equipo # Importamos el modelo de la otra app

class Paquete(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio_por_dia = models.DecimalField(max_digits=10, decimal_places=2)
    propietario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mis_paquetes')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

class PaqueteItem(models.Model):
    paquete = models.ForeignKey(Paquete, on_delete=models.CASCADE, related_name='items')
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.cantidad}x {self.equipo.titulo} en {self.paquete.titulo}"