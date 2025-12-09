from django.db import models
from django.contrib.auth.models import AbstractUser

# 1. TABLAS INDEPENDIENTES (Catálogos)
class Rol(models.Model):
    nombre = models.CharField(max_length=50) # Cliente, Propietario, Admin
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class Categoria(models.Model):
    nombre = models.CharField(max_length=100) # Sonido, Luces, Video

    def __str__(self):
        return self.nombre

# 2. USUARIO (Extendido con tu lógica)
class CustomUser(AbstractUser):
    # Campos base de Django ya incluidos (username, password, email, first_name...)
    # Tu diagrama pide Email único:
    email = models.EmailField(unique=True)
    
    # Relación con Rol (Hacemos null=True para no romper el createsuperuser)
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True, blank=True)
    
    
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    REQUIRED_FIELDS = ['email'] 

    def __str__(self):
        return self.username

# 3. EQUIPOS E INVENTARIO
class Equipo(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    foto_principal = models.URLField(blank=True, null=True) # URL de la imagen
    propietario = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='mis_equipos')
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
    cantidad_total = models.PositiveIntegerField(default=1) # Stock

# 4. PAQUETES
class Paquete(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio_por_dia = models.DecimalField(max_digits=10, decimal_places=2)
    propietario = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='mis_paquetes')

    def __str__(self):
        return self.titulo

class PaqueteItem(models.Model):
    paquete = models.ForeignKey(Paquete, on_delete=models.CASCADE, related_name='items')
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

# 5. RESERVAS 
class Reserva(models.Model):
    ESTADOS = [
        ('PENDIENTE', 'Pendiente'),
        ('APROBADO', 'Aprobado'),
        ('CANCELADO', 'Cancelado'),
        ('FINALIZADO', 'Finalizado'),
    ]
    
    cliente = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='mis_reservas')
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PENDIENTE')
    precio_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

class ReservaItem(models.Model):
    # Un item de reserva puede ser un Equipo individual O un Paquete
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE, related_name='items')
    tipo_item = models.CharField(max_length=20) # 'EQUIPO' o 'PAQUETE'
    
    # Claves foráneas opcionales (Una de las dos debe tener datos)
    equipo = models.ForeignKey(Equipo, on_delete=models.SET_NULL, null=True, blank=True)
    paquete = models.ForeignKey(Paquete, on_delete=models.SET_NULL, null=True, blank=True)
    
    cantidad = models.PositiveIntegerField()
    precio_capturado = models.DecimalField(max_digits=10, decimal_places=2) # Precio al momento de reservar

# 6. REVIEWS
class Review(models.Model):
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE)
    cliente = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    calificacion = models.PositiveIntegerField() # 1 a 5
    comentario = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)