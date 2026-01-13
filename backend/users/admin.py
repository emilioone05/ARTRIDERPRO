from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = (
        'email',
        'username',
        'account_type',
        'is_staff',
        'is_active',
    )

    fieldsets = UserAdmin.fieldsets + (
        ('Información adicional', {
            'fields': (
                'account_type',
                'phone_number',
                'company_name',
                'location',
                'description',
                'firebase_uid',
            )
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información adicional', {
            'fields': (
                'account_type',
            )
        }),
    )

    ordering = ('email',)
