from django.db import models
from django.conf import settings
from inventory.models import Publication, Unit, Package
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
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
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDIENTE')
    created_at = models.DateTimeField(auto_now_add=True)

    def update_total(self):
        if self.start_date and self.end_date:
            delta = self.end_date - self.start_date
            days = delta.days if delta.days > 0 else 1
        else:
            days = 1
        daily_total = 0 
        
        for item in self.items.all():
            if item.publication:
                daily_total += item.publication.price_per_day 
            
            elif item.package:
                if hasattr(item.package, 'price'): 
                     daily_total += item.package.price #(falta)

        self.total_price = daily_total * days
        
        self.save(update_fields=['total_price'])

    def __str__(self):
        return f"{self.reservation_code} - {self.client.email}"

class ReservationItem(models.Model):
    reservation = models.ForeignKey(Reservation, related_name='items', on_delete=models.CASCADE)
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, null=True, blank=True, on_delete=models.SET_NULL)
    assigned_unit = models.ForeignKey(Unit, null=True, blank=True, on_delete=models.SET_NULL)
    # LA CLAVE DEL QR:
    # assigned_unit = models.ForeignKey(Unit, null=True, blank=True, on_delete=models.SET_NULL)
    
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
@receiver(post_save, sender='bookings.ReservationItem') 
def recalc_price_on_save(sender, instance, created, **kwargs):
    # instance es el ReservationItem
    # instance.reservation es la Reserva padre
    instance.reservation.update_total()

# Signal si elimina un item de ReservationItem
@receiver(post_delete, sender='bookings.ReservationItem')
def recalc_price_on_delete(sender, instance, **kwargs):
    instance.reservation.update_total()