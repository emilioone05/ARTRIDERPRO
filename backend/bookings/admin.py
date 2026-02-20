from django.contrib import admin
from django import forms # <--- Necesitamos esto para personalizar el form
from .models import Reservation, ReservationItem
from inventory.models import Unit

# --- 1. FORMULARIO INTELIGENTE (El cerebro del filtro) ---
class ReservationItemForm(forms.ModelForm):
    class Meta:
        model = ReservationItem
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # LÓGICA DE FILTRADO DINÁMICO
        # Verificamos si esta fila ya existe (tiene un ID) y tiene una Publicación asignada
        if self.instance and self.instance.pk and self.instance.publication:
            # CASO A: Fila existente -> Mostramos solo unidades de ESA Publicación y DISPONIBLES
            self.fields['assigned_unit'].queryset = Unit.objects.filter(
                publication=self.instance.publication,
                status='DISPONIBLE'
            )
        else:
            # CASO B: Fila nueva o vacía -> Mostramos todo lo disponible (o nada, si prefieres)
            self.fields['assigned_unit'].queryset = Unit.objects.filter(status='DISPONIBLE')

# --- 2. CONFIGURACIÓN DE LOS ÍTEMS (Inlines) ---
class ReservationItemInline(admin.TabularInline):
    model = ReservationItem
    form = ReservationItemForm # <--- AQUI CONECTAMOS EL FORMULARIO INTELIGENTE
    extra = 0
    
    # Campos de solo lectura para evitar que cambien la publicación y rompan la lógica
    # (Opcional, pero recomendado para mantener la integridad)
    # readonly_fields = ('publication', 'package') 

# --- 3. CONFIGURACIÓN DE LA RESERVA ---
@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('reservation_code', 'client', 'start_date', 'status', 'total_price')
    list_filter = ('status', 'start_date')
    search_fields = ('reservation_code', 'client__email', 'client__username')
    
    inlines = [ReservationItemInline]

# --- 4. CONFIGURACIÓN ITEM SUELTO (Opcional) ---
@admin.register(ReservationItem)
class ReservationItemAdmin(admin.ModelAdmin):
    form = ReservationItemForm # Usamos el mismo form inteligente aquí también
    list_display = ('reservation', 'publication', 'assigned_unit', 'get_status')
    
    def get_status(self, obj):
        return obj.assigned_unit.status if obj.assigned_unit else "-"
    get_status.short_description = "Estado Unidad"