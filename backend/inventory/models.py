import uuid
from django.db import models
from django.conf import settings

# --- NIVEL 1: Catálogo Maestro ---
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class CatalogProduct(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    product_type = models.CharField(
        max_length=100, 
        blank=True, 
        help_text="Ej: Subwoofer Activo, Máquina de Humo, Pantalla LED"
    )
    specs = models.JSONField(default=dict, blank=True)
    image = models.ImageField(upload_to='catalog/', blank=True)

    def __str__(self):
        return f"{self.brand} {self.model} ({self.product_type})"

# --- NIVEL 2: Oferta Comercial ---
class Publication(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    catalog_product = models.ForeignKey(CatalogProduct, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    guarantee_amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Depósito de garantía")
    image = models.ImageField(upload_to='publications/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.title} ({self.owner.email})"
    # Para las
class PublicationImage(models.Model):
    publication = models.ForeignKey(Publication, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='publications_gallery/')
    created_at = models.DateTimeField(auto_now_add=True)
# --- NIVEL 3: Inventario Físico y QR ---
class Unit(models.Model):
    STATUS_CHOICES = (('DISPONIBLE', 'Disponible'), ('ALQUILADO', 'Alquilado'), ('MANTENIMIENTO', 'Mantenimiento'))
    
    publication = models.ForeignKey(Publication, related_name='units', on_delete=models.CASCADE)
    # EL QR SE GENERA AUTOMÁTICAMENTE AQUÍ
    qr_hash = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    serial_number = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DISPONIBLE')
    internal_notes = models.TextField(blank=True)

    def __str__(self):
        return f"Unit {self.serial_number} - {str(self.qr_hash)[:8]}"

class CalendarBlock(models.Model):
    unit = models.ForeignKey(Unit, related_name='blocks', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.CharField(max_length=100, default="MANTENIMIENTO")

# --- NIVEL 4: Paquetes ---
class Package(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

class PackageItem(models.Model):
    package = models.ForeignKey(Package, related_name='items', on_delete=models.CASCADE)
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)