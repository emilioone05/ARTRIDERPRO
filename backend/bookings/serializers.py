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
        read_only_fields = ('reservation_code', 'status')

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