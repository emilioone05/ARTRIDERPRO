from django.contrib import admin
from .models import (
    Category, CatalogProduct, Publication, 
    Unit, CalendarBlock, Package, PackageItem
)

# --- INLINES (Tablas dentro de otras tablas) ---

class UnitInline(admin.TabularInline):
    model = Unit
    extra = 1
    readonly_fields = ('qr_hash',) # Para ver el UUID pero no editarlo
    fields = ('serial_number', 'status', 'qr_hash', 'internal_notes')

class PackageItemInline(admin.TabularInline):
    model = PackageItem
    extra = 1
    autocomplete_fields = ['publication'] # Ayuda si tienes muchas publicaciones

# --- ADMINS PRINCIPALES ---

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(CatalogProduct)
class CatalogProductAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'category')
    list_filter = ('category', 'brand')
    search_fields = ('brand', 'model')

@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'price_per_day', 'get_stock_count', 'is_active')
    list_filter = ('is_active', 'owner')
    search_fields = ('title', 'owner__email')
    inlines = [UnitInline] # ¡Aquí ves las unidades físicas directo en el anuncio!

    def get_stock_count(self, obj):
        return obj.units.filter(status='DISPONIBLE').count()
    get_stock_count.short_description = 'Stock Disp.'

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('serial_number', 'publication', 'status', 'short_qr')
    list_filter = ('status', 'publication__catalog_product__category')
    search_fields = ('serial_number', 'qr_hash', 'publication__title')
    readonly_fields = ('qr_hash',)

    def short_qr(self, obj):
        return str(obj.qr_hash)[:8] + "..."
    short_qr.short_description = 'QR Hash'

@admin.register(CalendarBlock)
class CalendarBlockAdmin(admin.ModelAdmin):
    list_display = ('unit', 'start_date', 'end_date', 'reason')
    list_filter = ('reason',)

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'price_per_day')
    inlines = [PackageItemInline]