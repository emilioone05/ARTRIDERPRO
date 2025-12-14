from django.db import models
from django.conf import settings
from reservations.models import Reserva

class Review(models.Model):
    reserva = models.OneToOneField(Reserva, on_delete=models.CASCADE) # Una reseña por reserva
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    calificacion = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)]) # 1 a 5
    comentario = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review {self.calificacion}* de {self.autor.username}"