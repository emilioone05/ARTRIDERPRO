from rest_framework import serializers
from .models import Category, CatalogProduct, Publication, Unit, Package, PackageItem

# --- NIVEL 1: Unidades Físicas ---
class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = '__all__'
        read_only_fields = ('qr_hash', 'status') # El QR y estado se manejan internamente

# --- NIVEL 2: Publicaciones (Oferta Comercial) ---
class PublicationSerializer(serializers.ModelSerializer):
    # Mostramos las unidades anidadas para ver cuáles pertenecen a este anuncio
    units = UnitSerializer(many=True, read_only=True)
    # Campo calculado para saber cuántos hay libres
    stock_count = serializers.SerializerMethodField()

    class Meta:
        model = Publication
        fields = '__all__'
        read_only_fields = ('owner',) # El dueño se asigna automático en la vista

    def get_stock_count(self, obj):
        # Cuenta cuántas unidades están en estado 'DISPONIBLE'
        return obj.units.filter(status='DISPONIBLE').count()

# --- NIVEL 3: Paquetes (Bundles) ---

class PackageItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageItem
        fields = ['id', 'publication', 'quantity']

class PackageSerializer(serializers.ModelSerializer):
    # Esto permite que envíes los items DENTRO del JSON del paquete
    items = PackageItemSerializer(many=True)

    class Meta:
        model = Package
        fields = ['id', 'owner', 'name', 'price_per_day', 'description', 'items']
        read_only_fields = ('owner',) # El dueño se asigna automático

    # --- LÓGICA DE ESCRITURA ANIDADA (NESTED WRITE) ---
    def create(self, validated_data):
        # 1. Sacamos la lista de items del JSON
        items_data = validated_data.pop('items')
        
        # 2. Creamos el Paquete "padre"
        package = Package.objects.create(**validated_data)
        
        # 3. Recorremos la lista y creamos los items vinculados
        for item_data in items_data:
            PackageItem.objects.create(package=package, **item_data)
            
        return package