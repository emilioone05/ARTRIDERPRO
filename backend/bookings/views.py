from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db import transaction 

from .models import Reservation, ReservationItem
from inventory.models import Unit
from .serializers import ReservationSerializer, ScanQRSerializer, ProviderReservationListSerializer,ClientReservationListSerializer

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    # serializer_class = ReservationSerializer
    def get_serializer_class(self):
        # 1. Crear o Actualizar: Serializer completo
        if self.action in ['create', 'update', 'partial_update']:
            return ReservationSerializer
        
        # 2. Listar o Ver Detalle
        if self.action in ['list', 'retrieve']:
            mode = self.request.query_params.get('mode')
            
            # Si estoy en modo proveedor -> lo manda al serializer del proveedor
            if mode == 'provider':
                return ProviderReservationListSerializer
            
            # Si estoy en modo cliente -> Lo manda al Serializer del modo "Cliente"
            return ClientReservationListSerializer
            
        return ReservationSerializer
    def get_queryset(self):
        user = self.request.user
        
        if not user.is_authenticated:
            return Reservation.objects.none()

        mode = self.request.query_params.get('mode')

        if mode == 'provider':
            # --- MODO PROVEEDOR ---
            return Reservation.objects.filter(
                items__publication__owner=user 
            ).distinct().order_by('-created_at')
        
        else:
            # --- MODO CLIENTE ---
            return Reservation.objects.filter(
                client=user
            ).order_by('-created_at')
    # ENDPOINT POST /api/reservas/scan_delivery/
    @action(detail=False, methods=['post'])
    def scan_delivery(self, request):
        serializer = ScanQRSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        res_id = serializer.validated_data['reservation_id']
        qr_uuid = serializer.validated_data['qr_code']

        # 1. Buscar la Reserva y la Unidad
        try:
            reservation = Reservation.objects.get(id=res_id)
            unit = Unit.objects.get(qr_hash=qr_uuid)
        except (Reservation.DoesNotExist, Unit.DoesNotExist):
            return Response({"error": "Reserva o Código QR no encontrados"}, status=404)

        # 2. VALIDACIÓN DE SEGURIDAD (Dueño)
        # Aquí corregimos el 'pass'. Si no es el dueño, FUERA.
        if unit.publication.owner != request.user:
             return Response(
                 {"error": "No tienes permiso para gestionar este equipo. No te pertenece."}, 
                 status=status.HTTP_403_FORBIDDEN
             )

        # 3. Validar: ¿La unidad pertenece al producto reservado?
        # Buscamos un item en esta reserva que pida este tipo de producto y NO tenga unidad asignada aun
        item_pendiente = ReservationItem.objects.filter(
            reservation=reservation,
            publication=unit.publication, # <--- EL MATCH CRUCIAL (Evita mezclar peras con manzanas)
            assigned_unit__isnull=True
        ).first()

        if not item_pendiente:
            # Mensaje amable explicando el error
            return Response({
                "error": "Equipo incorrecto o ya completado. " 
                         f"Escaneaste un '{unit.publication.title}', "
                         "pero la reserva no tiene pendientes de ese tipo."
            }, status=400)

        # 4. ÉXITO: Transacción Atómica (Todo o Nada)
        try:
            with transaction.atomic():
                # A. Asignar unidad al item de la reserva
                item_pendiente.assigned_unit = unit
                item_pendiente.scanned_at_pickup = timezone.now()
                item_pendiente.save()

                # B. Cambiar estado físico de la unidad
                unit.status = 'ALQUILADO'
                unit.save()

                # C. Si la reserva estaba 'Confirmada' (o pendiente), pasa a 'En Curso'
                # Nota: Verifica que 'EN_CURSO' sea exacto como lo pusiste en tus choices de models.py
                if reservation.status != 'EN_CURSO':
                    reservation.status = 'EN_CURSO'
                    reservation.save()

        except Exception as e:
            return Response({"error": f"Error al guardar datos: {str(e)}"}, status=500)

        return Response({
            "message": "¡Match correcto! Equipo entregado.",
            "unit": unit.serial_number,
            "publication": unit.publication.title
        })
    def get_serializer_class(self):
        # Si se crea o modifica, usamos el serializer Reservaion 
        if self.action in ['create', 'update', 'partial_update']:
            return ReservationSerializer
        
        # LISTANDO (GET)
        if self.action == 'list':
            mode = self.request.query_params.get('mode')
            # modo proveedor,serializer detallado con datos de cliente (provider)
            if mode == 'provider':
                return ProviderReservationListSerializer
            # modo normal serializercliente
            return ClientReservationListSerializer
            
        # Para detalle (retrieve), usamos el del cliente por defecto o el que se seleccione (aun no lo termino)
        return ClientReservationListSerializer

    def get_queryset(self):
        user = self.request.user
        # Si el usuario no está logueado, no devuelve nada (seguridad)
        if not user.is_authenticated:
            return Reservation.objects.none()

        # Obtenemos el parámetro de la URL: ?mode=provider
        mode = self.request.query_params.get('mode')

        if mode == 'provider':
            # --- QUERYSET PROVEEDOR ---
            # " reservas que contienen items (equipos) que le pertenecen al proveedor"
            return Reservation.objects.filter(
                items__publication__owner=user
            ).distinct().order_by('-created_at')
        
        else:
            # --- QUERYSET CLIENTE ---
            # "reservas que hice en modo cliente"
            return Reservation.objects.filter(
                client=user
            ).order_by('-created_at')   
