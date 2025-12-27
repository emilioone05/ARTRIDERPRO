from django.db import models
from django.conf import settings
from inventory.models import Publication, Unit, Package
from django.core.exceptions import ValidationError

class Reservation(models.Model):
    STATUS_CHOICES = (
        ('PENDIENTE', 'Pendiente Confirmación'),
        ('CONFIRMADA', 'Confirmada'),
        ('EN_CURSO', 'En Curso (Equipos entregados)'),
        ('FINALIZADA', 'Finalizada'),
    )
    
    reservation_code = models.CharField(max_length=20, unique=True) # Ej: RES-001
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDIENTE')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reservation_code} - {self.client.email}"

class ReservationItem(models.Model):
    reservation = models.ForeignKey(Reservation, related_name='items', on_delete=models.CASCADE)
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, null=True, blank=True, on_delete=models.SET_NULL)
    assigned_unit = models.ForeignKey(Unit, null=True, blank=True, on_delete=models.SET_NULL)
    # LA CLAVE DEL QR:
    assigned_unit = models.ForeignKey(Unit, null=True, blank=True, on_delete=models.SET_NULL)
    
    scanned_at_pickup = models.DateTimeField(null=True, blank=True)
    scanned_at_return = models.DateTimeField(null=True, blank=True)
    
    def clean(self):
        # ... tu validación de tipos (Subwoofer vs Parlante) ...
        if self.assigned_unit:
            if self.assigned_unit.publication != self.publication:
                raise ValidationError(...) # Tu mensaje de error

    def save(self, *args, **kwargs):
        # 1. Ejecutamos la validación
        self.clean() 
        
        # 2. MAGIA NUEVA: Actualización Automática de la Unidad
        # Si este item ya tiene una unidad asignada...
        if self.assigned_unit:
            # ... vamos a esa unidad y le cambiamos el estado a ALQUILADO
            self.assigned_unit.status = 'ALQUILADO'
            self.assigned_unit.save()
        
        # 3. Guardamos el item normalmente
        super().save(*args, **kwargs)