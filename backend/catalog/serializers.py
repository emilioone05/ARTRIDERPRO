from rest_framework import serializers
from .models import Equipo, Inventario, Categoria, FotoEquipo

class InventarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventario
        fields = ['precio_por_dia', 'cantidad_total']

class EquipoSerializer(serializers.ModelSerializer):
    inventario = InventarioSerializer() # Nested serializer
    
    class Meta:
        model = Equipo
        fields = ['id', 'titulo', 'descripcion', 'foto_principal', 'categoria', 'inventario']

    def create(self, validated_data):
            # Sacamos los datos del inventario para usarlos aparte
            inventario_data = validated_data.pop('inventario')
            
            # CORRECCIÓN: Quitamos "propietario=user" de aquí dentro.
            # Como ya lo pasamos desde la View (views.py), ya viene incluido en **validated_data
            equipo = Equipo.objects.create(**validated_data)
            
            # Crear el inventario vinculado
            Inventario.objects.create(equipo=equipo, **inventario_data)
            
            return equipo