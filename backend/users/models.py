from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):

    ACCOUNT_TYPES = (
        ('cliente', 'Cliente'),
        ('proveedor', 'Proveedor'),
        ('admin', 'Administrador'),
    )
    full_name = models.CharField(max_length=255, blank=True, null=True)
    firebase_uid = models.CharField(
        max_length=128,
        unique=True,
        null=True,
        blank=True
    )

    email = models.EmailField(unique=True)

    account_type = models.CharField(
        max_length=20,
        choices=ACCOUNT_TYPES,
        default='cliente'
    )

    phone_number = models.CharField(max_length=15, blank=True, null=True)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'full_name']

    def __str__(self):
        return self.email
