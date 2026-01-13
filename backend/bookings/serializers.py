from rest_framework import serializers
from .models import Reservation, ReservationItem
from inventory.models import Package, Publication, Unit 
import uuid
from django.db.models import Q

# --- 1. SERIALIZER PARA EL ESCANEO (IGUAL) ---
class ScanQRSerializer(serializers.Serializer):
    reservation_id = serializers.IntegerField()
    qr_code = serializers.CharField()

# --- 2. SERIALIZER DE ITEMS (AQUÍ ESTÁ EL ARREGLO) ---
class ReservationItemSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(default=1, write_only=True)

    class Meta:
        model = ReservationItem
        fields = ['id', 'publication', 'package', 'assigned_unit', 'quantity']
        read_only_fields = ('assigned_unit',)
        
        # EL TRUCO: Decimos que publication y package son opcionales en la entrada
        extra_kwargs = {
            'publication': {'required': False, 'allow_null': True},
            'package': {'required': False, 'allow_null': True},
        }
    # VALIDACIÓN MANUAL: Aseguramos que manden AL MENOS UNO de los dos
    def validate(self, data):
        # Si no hay publicación Y no hay paquete -> Error
        if not data.get('publication') and not data.get('package'):
            raise serializers.ValidationError("Debes especificar una Publicación ID o un Paquete ID.")
        return data

# --- 3. SERIALIZER DE RESERVA (TU LÓGICA DE DESEMPAQUETADO) ---
class ReservationSerializer(serializers.ModelSerializer):
    items = ReservationItemSerializer(many=True)

    class Meta:
        model = Reservation
        fields = ['id', 'reservation_code', 'client', 'start_date', 'end_date', 'total_price', 'status', 'items']
        read_only_fields = ('reservation_code', 'status','total_price')

    def validate(self, data):
        """
        AQUÍ EVITAMOS EL OVERBOOKING
        Calculamos si hay stock suficiente para las fechas solicitadas.
        """
        start_date = data['start_date']
        end_date = data['end_date']
        items_payload = data['items']

        # 1. DESGLOSAR QUÉ NECESITA ESTA NUEVA RESERVA
        # Creamos un diccionario: { publication_id: cantidad_necesaria }
        requirements = {}

        for item in items_payload:
            qty = item.get('quantity', 1)
            
            # A. Si pide un Paquete, sumamos sus componentes
            if item.get('package'):
                package_obj = item.get('package')
                # Recorremos los ingredientes del paquete
                for p_item in package_obj.items.all():
                    pub_id = p_item.publication.id
                    needed = p_item.quantity * qty
                    requirements[pub_id] = requirements.get(pub_id, 0) + needed
            
            # B. Si pide una Publicación suelta
            elif item.get('publication'):
                pub_obj = item.get('publication')
                requirements[pub_obj.id] = requirements.get(pub_obj.id, 0) + qty

        # 2. VERIFICAR DISPONIBILIDAD EN BASE DE DATOS PARA CADA PRODUCTO
        for pub_id, qty_needed in requirements.items():
            # A. Total de Unidades Físicas que "Sirven" (Excluyendo Mantenimiento/Baja)
            total_stock = Unit.objects.filter(
                publication_id=pub_id
            ).exclude(status__in=['MANTENIMIENTO', 'BAJA', 'ROBADO']).count()

            # B. Unidades que YA están ocupadas en esas fechas por OTRAS reservas
            # Buscamos reservas que se solapen con las fechas solicitadas
            # Lógica de solapamiento: (StartA < EndB) and (EndA > StartB)
            overlapping_reservations = Reservation.objects.filter(
                start_date__lt=end_date,
                end_date__gt=start_date
            ).exclude(status__in=['CANCELADA', 'FINALIZADA']) # Ignoramos las canceladas

            # Contamos cuántos items de este producto están en esas reservas solapadas
            occupied_count = ReservationItem.objects.filter(
                reservation__in=overlapping_reservations,
                publication_id=pub_id
            ).count()

            available_stock = total_stock - occupied_count

            # C. El Veredicto Final
            if available_stock < qty_needed:
                pub_name = Publication.objects.get(id=pub_id).title
                raise serializers.ValidationError(
                    f"No hay stock suficiente de '{pub_name}' para estas fechas. "
                    f"Total: {total_stock}, Ocupados: {occupied_count}, Disponibles: {available_stock}. "
                    f"Tú pediste: {qty_needed}."
                )

        return data

    def create(self, validated_data):
        # ... (Tu código create anterior sigue EXACTAMENTE IGUAL aquí abajo) ...
        # (Copia el método create que ya tenías y que funcionaba bien)
        items_data = validated_data.pop('items')
        start_date = validated_data['start_date']
        end_date = validated_data['end_date']
        delta = end_date - start_date
        days = delta.days if delta.days > 0 else 1
        daily_total = 0
        for item in items_data:
            qty = item.get('quantity', 1)
            
            # Caso A: Es una Publicación suelta
            if 'publication' in item and item['publication']:
                # Django DRF ya nos da el objeto Publication aquí, accedemos a su precio
                price = item['publication'].price_per_day
                daily_total += price * qty
            
            # Caso B: Es un Paquete
            elif 'package' in item and item['package']:
                # Asumiendo que el paquete tiene un precio base o sumamos sus items
                # Opción 1: El paquete tiene precio fijo (Recomendado)
                if hasattr(item['package'], 'price_per_day'):
                     daily_total += item['package'].price_per_day * qty
                # Opción 2: Si el precio es la suma de sus componentes (más complejo, usa Opción 1 si puedes)
                else:
                     # Lógica alternativa si el paquete no tiene precio directo
                     pass 

        # 3. ASIGNAR EL PRECIO TOTAL CALCULADO
        # (Precio diario * Días)
        validated_data['total_price'] = daily_total * days

        if 'reservation_code' not in validated_data:
            validated_data['reservation_code'] = f"RES-{str(uuid.uuid4())[:8].upper()}"

        reservation = Reservation.objects.create(**validated_data)

        for item_data in items_data:
            qty = item_data.pop('quantity', 1)
            
            if 'package' in item_data and item_data['package']:
                package_obj = item_data['package']
                package_contents = package_obj.items.all()
                for _ in range(qty):
                    for p_item in package_contents:
                        for _ in range(p_item.quantity):
                            ReservationItem.objects.create(
                                reservation=reservation,
                                publication=p_item.publication,
                                package=package_obj,
                                assigned_unit=None
                            )
            elif 'publication' in item_data and item_data['publication']:
                for _ in range(qty):
                    ReservationItem.objects.create(reservation=reservation, **item_data)

        return reservation
# --- 4. SERIALIZERS AUXILIARES PARA LECTURA (UI) ---

class SimpleUserSerializer(serializers.ModelSerializer):
    """Para mostrar datos básicos del cliente al proveedor"""
    class Meta:
        # Ajusta 'CustomUser' según cómo se llame tu modelo importado
        from django.contrib.auth import get_user_model
        model = get_user_model()
        fields = ['id', 'full_name', 'email', 'phone_number']

class SimpleItemSerializer(serializers.ModelSerializer):
    """Para mostrar el equipo/producto dentro de la tarjeta de reserva"""
    title = serializers.CharField(source='publication.title',read_only=True)
    image = serializers.SerializerMethodField()
    price_per_day = serializers.DecimalField(source='publication.price_per_day', max_digits=10, decimal_places=2,read_only=True)
    
    class Meta:
        model = ReservationItem
        fields = [
            'id', 
            'title',          
            'publication', 
            'assigned_unit', 
            'scanned_at_pickup', 
            'scanned_at_return',
            'price_per_day',
            'image'
        ]
    def get_image(self, obj):
        # Validación defensiva: Si no hay publicación o imagen, retorna None
        if obj.publication and hasattr(obj.publication, 'image') and obj.publication.image:
            try:
                return obj.publication.image.url
            except ValueError:
                return None
        return None
    # def get_image(self, obj):
    #     # CORRECCIÓN DE SEGURIDAD:
    #     # Verificamos que exista publication y que tenga imagen antes de pedir la URL
    #     if obj.publication and obj.publication.image:
    #         try:
    #             return obj.publication.image.url
    #         except ValueError:
    #             return None
    #     return None

# --- 5. SERIALIZER PARA LA VISTA "MODO CLIENTE" (Tu segunda imagen) ---
class ClientReservationListSerializer(serializers.ModelSerializer):
    """
    Lo que ve el usuario normal: Qué alquiló, fechas, estado y total.
    """
    first_item_name = serializers.SerializerMethodField()
    first_item_image = serializers.SerializerMethodField()
    item_count = serializers.SerializerMethodField()

    class Meta:
        model = Reservation
        fields = [
            'id', 'reservation_code', 'start_date', 'end_date', 
            'total_price', 'status', 'first_item_name', 'first_item_image', 'item_count'
        ]

    def get_first_item_name(self, obj):
        # Obtiene el nombre del primer equipo para el título de la tarjeta
        item = obj.items.first()
        if item:
            return item.publication.title
        return "Reserva sin items"

    def get_first_item_image(self, obj):
        item = obj.items.first()
        if item and item.publication.image:
            return item.publication.image.url
        return None
    
    def get_item_count(self, obj):
        return obj.items.count()

# --- 6. SERIALIZER PARA LA VISTA "MODO PROVEEDOR" (Tu primera imagen) ---
class ProviderReservationListSerializer(serializers.ModelSerializer):
    """
    Lo que ve el dueño de los equipos: Datos del cliente y cuánto ganará.
    """
    client = SimpleUserSerializer(read_only=True)
    items = SimpleItemSerializer(many=True, read_only=True)
    days_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Reservation
        fields = [
            'id', 'reservation_code', 'start_date', 'end_date', 'status', 
            'total_price', 'client', 'items', 'days_count'
        ]

    def get_days_count(self, obj):
        delta = obj.end_date - obj.start_date
        return delta.days if delta.days > 0 else 1