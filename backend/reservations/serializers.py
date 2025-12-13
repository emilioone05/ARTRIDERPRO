from rest_framework import serializers
from django.db.models import Sum, Q
from .models import Reserva, ReservaItem
from catalog.models import Equipo
from packages.models import Paquete

class ReservaItemSerializer(serializers.ModelSerializer):
    equipo_id = serializers.PrimaryKeyRelatedField(
        queryset=Equipo.objects.all(), source='equipo', required=False, allow_null=True
    )
    paquete_id = serializers.PrimaryKeyRelatedField(
        queryset=Paquete.objects.all(), source='paquete', required=False, allow_null=True
    )

    class Meta:
        model = ReservaItem
        fields = ['equipo_id', 'paquete_id', 'cantidad', 'precio_capturado']

class ReservaSerializer(serializers.ModelSerializer):
    items = ReservaItemSerializer(many=True)

    class Meta:
        model = Reserva
        fields = ['id', 'cliente', 'propietario', 'fecha_inicio', 'fecha_fin', 'estado', 'precio_total', 'items']
        read_only_fields = ['cliente', 'estado', 'precio_total'] # El precio lo calcula el backend

    def validate(self, data):
        """
        VALIDACIÓN DE STOCK (F-404): Verifica que los equipos estén libres en esas fechas.
        """
        inicio = data['fecha_inicio']
        fin = data['fecha_fin']
        items = data['items']

        for item in items:
            cantidad_solicitada = item.get('cantidad', 1)
            equipo = item.get('equipo')
            
            # Si es un equipo individual, validamos su stock
            if equipo:
                stock_total = equipo.inventario.cantidad_total
                
                # Buscamos reservas APROBADAS que se crucen con estas fechas
                reservas_ocupadas = ReservaItem.objects.filter(
                    equipo=equipo,
                    reserva__estado='APROBADO',
                    reserva__fecha_inicio__lt=fin,
                    reserva__fecha_fin__gt=inicio
                ).aggregate(total_ocupado=Sum('cantidad'))
                
                ocupado = reservas_ocupadas['total_ocupado'] or 0
                disponible = stock_total - ocupado
                
                if cantidad_solicitada > disponible:
                    raise serializers.ValidationError(
                        f"No hay stock suficiente para '{equipo.titulo}'. Solicitado: {cantidad_solicitada}, Disponible: {disponible}"
                    )
        
        return data

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context['request'].user
        
        # Calcular precio total automatico
        total = 0
        for item in items_data:
            total += item['precio_capturado'] * item['cantidad']

        reserva = Reserva.objects.create(
            precio_total=total,
            **validated_data
        )

        for item_data in items_data:
            ReservaItem.objects.create(reserva=reserva, **item_data)
            
        return reserva