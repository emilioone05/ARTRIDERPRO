from rest_framework import serializers
from .models import Paquete, PaqueteItem
from catalog.models import Equipo

class PaqueteItemSerializer(serializers.ModelSerializer):
    # Esto muestra el nombre del equipo en lugar de solo el ID al leer
    equipo_titulo = serializers.ReadOnlyField(source='equipo.titulo')
    equipo_id = serializers.PrimaryKeyRelatedField(
        queryset=Equipo.objects.all(), source='equipo', write_only=True
    )

    class Meta:
        model = PaqueteItem
        fields = ['id', 'equipo_id', 'equipo_titulo', 'cantidad']

class PaqueteSerializer(serializers.ModelSerializer):
    items = PaqueteItemSerializer(many=True) # Nested: Manda los items dentro del paquete

    class Meta:
        model = Paquete
        fields = ['id', 'titulo', 'descripcion', 'precio_por_dia', 'items', 'created_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context['request'].user
        
        # Crear el Paquete
        paquete = Paquete.objects.create(**validated_data)
        
        # Crear los Items del paquete
        for item_data in items_data:
            PaqueteItem.objects.create(paquete=paquete, **item_data)
            
        return paquete