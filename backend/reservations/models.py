from django.db import models
from django.conf import settings
from catalog.models import Equipo
from packages.models import Paquete

class Reserva(models.Model):
    ESTADOS = [
        ('PENDIENTE', 'Pendiente'),
        ('APROBADO', 'Aprobado'),
        ('RECHAZADO', 'Rechazado'),
        ('FINALIZADO', 'Finalizado'),
        ('CANCELADO', 'Cancelado'),
    ]
    
    cliente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mis_reservas')
    # El propietario se puede inferir de los items, pero para simplificar MVP asumimos reservas por propietario unico o mixto.
    # Para hacerlo facil: una reserva puede tener items de varios dueños, O restringimos a un dueño por reserva. 
    # Modelo Uber/Airbnb: 1 Reserva = 1 Propietario. Vamos a simplificarlo asi para evitar conflictos.
    propietario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='solicitudes_reserva')
    
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PENDIENTE')
    precio_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reserva #{self.id} - {self.cliente.email}"

class ReservaItem(models.Model):
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE, related_name='items')
    
    # Puede ser Equipo O Paquete (Uno de los dos debe tener datos)
    equipo = models.ForeignKey(Equipo, on_delete=models.SET_NULL, null=True, blank=True)
    paquete = models.ForeignKey(Paquete, on_delete=models.SET_NULL, null=True, blank=True)
    
    cantidad = models.PositiveIntegerField(default=1)
    precio_capturado = models.DecimalField(max_digits=10, decimal_places=2) # Precio al momento de reservar (Congelado)

    def __str__(self):
        item_name = self.equipo.titulo if self.equipo else (self.paquete.titulo if self.paquete else "Desconocido")
        return f"{self.cantidad}x {item_name}"