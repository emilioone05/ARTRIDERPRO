from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLES = (
        ('ADMIN', 'Admin'),
        ('PROPIETARIO', 'Propietario'),
        ('CLIENTE', 'Cliente'),
    )
    # Campos existentes
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, verbose_name="Teléfono")
    role = models.CharField(max_length=20, choices=ROLES, default='CLIENTE')
    city = models.CharField(max_length=100, blank=True, verbose_name="Ciudad")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="Foto de Perfil")
    
    # NUEVO CAMPO (según tu diagrama)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone']

    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"