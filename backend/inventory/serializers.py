from rest_framework import serializers
from .models import (
    Category, CatalogProduct, Publication, PublicationImage, 
    Unit, Package, PackageItem
)

# --- AUXILIARES: Para mostrar detalles legibles (No solo IDs) ---

class PublicationImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicationImage
        fields = ['id', 'image']

class CatalogProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    class Meta:
        model = CatalogProduct
        fields = ['id', 'brand', 'model', 'product_type', 'image', 'specs', 'category_name']

# --- NIVEL GLOBAL: Tarjeta de Resumen (Feed Principal) ---

class CatalogItemSerializer(serializers.Serializer):
    """
    Este serializer unifica Publicaciones y Paquetes para la vista principal (Cards).
    Soluciona el problema de las imágenes rotas generando URLs absolutas.
    """
    id = serializers.IntegerField()
    title = serializers.CharField() 
    description = serializers.CharField()
    pricePerDay = serializers.DecimalField(max_digits=10, decimal_places=2, source='price_per_day')
    image = serializers.SerializerMethodField()
    stock = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    def get_image(self, obj):
        request = self.context.get('request')
        image_field = None

        # 1. Lógica para Publicaciones (Equipos)
        if isinstance(obj, Publication):
            # Prioridad A: Imagen específica de la publicación (estado real del equipo)
            if obj.image:
                image_field = obj.image
            # Prioridad B: Imagen de catálogo (foto de internet/stock)
            elif obj.catalog_product.image:
                image_field = obj.catalog_product.image
        
        # 2. Lógica para Paquetes
        elif isinstance(obj, Package):
            # Intentamos tomar la imagen del primer item del paquete
            first_item = obj.items.first()
            if first_item:
                # Revisamos si esa publicación tiene imagen propia o de catálogo
                pub = first_item.publication
                if pub.image:
                    image_field = pub.image
                elif pub.catalog_product.image:
                    image_field = pub.catalog_product.image

        # 3. Construcción de URL ANGULAR
        if image_field and hasattr(image_field, 'url'):
            if request:
                return request.build_absolute_uri(image_field.url)
            return image_field.url # Fallback si no hay request context

        return "https://via.placeholder.com/600x400?text=Sin+Imagen"

    def get_stock(self, obj):
        if isinstance(obj, Publication):
            return obj.units.filter(status='DISPONIBLE').count()
        elif isinstance(obj, Package):
            #(FALTA) logica de inventario cruzado 
            return 1 
        return 0

    def get_type(self, obj):
        return 'equipo' if isinstance(obj, Publication) else 'paquete'

    def get_category(self, obj):
        if isinstance(obj, Publication):
            return obj.catalog_product.category.name
        return "Paquete"

# --- NIVEL 1: Unidades Físicas ---

class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = '__all__'
        read_only_fields = ('qr_hash', 'status') 

# --- NIVEL 2: Publicaciones

class PublicationSerializer(serializers.ModelSerializer):
    product_details = CatalogProductSerializer(source='catalog_product', read_only=True)
    gallery = PublicationImageSerializer(source='images', many=True, read_only=True)
    units = UnitSerializer(many=True, read_only=True)
    stock_count = serializers.SerializerMethodField()
    owner_email = serializers.CharField(source='owner.email', read_only=True)

    stock = serializers.IntegerField(write_only=True, default=1)
    brand = serializers.CharField(write_only=True)
    model = serializers.CharField(write_only=True)
    category = serializers.IntegerField(write_only=True) 
    catalog_product = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Publication
        fields = [
            'id', 'owner', 'owner_email', 
            'catalog_product', 'product_details',
            'title', 'description', 
            'price_per_day', 'guarantee_amount', 
            'image', 'gallery', 
            'is_active', 'stock_count', 'units',
            'stock', 'brand', 'model', 'category'
        ]
        read_only_fields = ('owner',)

    def get_stock_count(self, obj):
        return obj.units.filter(status='DISPONIBLE').count()
    def create(self, validated_data):
        # 1. Sacamos los datos que NO son de la tabla Publicación
        stock_qty = validated_data.pop('stock', 1)
        brand = validated_data.pop('brand')
        model = validated_data.pop('model')
        category_id = validated_data.pop('category')
        
        # 2. Buscamos o Creamos el Producto de Catálogo (Para no repetir)
        # Esto evita tener 50 veces "Canon T7" en la base de datos
        category_obj = Category.objects.get(id=category_id)
        
        product, created = CatalogProduct.objects.get_or_create(
            brand=brand, 
            model=model,
            defaults={
                'category': category_obj,
                'specs': validated_data.get('description', '')
            }
        )

        # 3. Creamos la Publicación vinculada a ese producto
        publication = Publication.objects.create(
            catalog_product=product, 
            **validated_data
        )

        # 4. Creamos las Unidades (El Stock físico)
        units_list = []
        for i in range(stock_qty):
            units_list.append(Unit(
                publication=publication,
                status='DISPONIBLE',
                serial_number=f"GEN-{publication.id}-{i+1}"
            ))
        Unit.objects.bulk_create(units_list)

        return publication

# --- NIVEL 3: Paquetes (Bundles) ---

class PackageItemSerializer(serializers.ModelSerializer):
    # Para mostrar el nombre del equipo en el detalle del paquete
    publication_title = serializers.CharField(source='publication.title', read_only=True)
    
    class Meta:
        model = PackageItem
        fields = ['id', 'publication', 'publication_title', 'quantity']

class PackageSerializer(serializers.ModelSerializer):
    items = PackageItemSerializer(many=True)

    class Meta:
        model = Package
        fields = ['id', 'owner', 'name', 'price_per_day', 'description', 'items']
        read_only_fields = ('owner',)

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        package = Package.objects.create(**validated_data)
        for item_data in items_data:
            PackageItem.objects.create(package=package, **item_data)
        return package

# --- NIVEL 4: Estadísticas ---

class ProviderHomeStatsSerializer(serializers.Serializer):
    company_name = serializers.CharField()
    email = serializers.EmailField()
    phone = serializers.CharField()
    location = serializers.CharField()
    published_equipments = serializers.IntegerField()
    active_reservations = serializers.IntegerField()
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']