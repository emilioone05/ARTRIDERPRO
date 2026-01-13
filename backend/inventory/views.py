from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.routers import DefaultRouter
from rest_framework.permissions import AllowAny
# IMPORTA TUS MODELOS (Solo los que existen en inventory)
from .models import Publication, Unit, Package
from .models import Category
# IMPORTA TUS SERIALIZERS
from .serializers import (
    PublicationSerializer, 
    UnitSerializer, 
    PackageSerializer,
    CatalogItemSerializer,      
    ProviderHomeStatsSerializer,
    CategorySerializer
)

# --- VIEWSETS ESTÁNDAR (CRUD) ---

class PublicationViewSet(viewsets.ModelViewSet):
    queryset = Publication.objects.filter(is_active=True)
    serializer_class = PublicationSerializer
    permission_classes = [IsAuthenticated] 

    def create(self, request, *args, **kwargs):
        # Validación de seguridad (Permiso)
        current_type = getattr(request.user, 'account_type', '')
        if str(current_type).lower() != 'proveedor':
             return Response({"error": "Solo proveedores pueden publicar."}, status=403)
             
        # Ya no hace falta perform_create, el serializer lo hace todo
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        # Solo necesitamos pasar el usuario dueño
        serializer.save(owner=self.request.user)    

class UnitViewSet(viewsets.ModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    
class PackageViewSet(viewsets.ModelViewSet):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# --- VISTAS DEL PROVEEDOR (CATÁLOGO Y HOME) ---

class ProviderCatalogView(APIView):
    """
    URL: /api/inventory/provider/catalog/
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # 1. Obtener datos
        publications = Publication.objects.filter(owner=user, is_active=True).select_related('catalog_product', 'catalog_product__category')
        packages = Package.objects.filter(owner=user).prefetch_related('items__publication__catalog_product')

        # 2. Calcular Estadísticas
        total_items = publications.count()
        total_packages = packages.count()
        total_stock = Unit.objects.filter(publication__owner=user, status='DISPONIBLE').count()

        # 3. Combinar y Serializar
        combined_list = list(publications) + list(packages)
        
        serializer = CatalogItemSerializer(combined_list, many=True, context={'request': request})

        return Response({
            "stats": {
                "totalItems": total_items,
                "totalStock": total_stock,
                "totalPackages": total_packages
            },
            "items": serializer.data
        })        

class ProviderHomeView(APIView):
    """
    URL: /api/inventory/provider/home/
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        
        equipment_count = Publication.objects.filter(owner=user, is_active=True).count()
        
        # --- CORRECCIÓN AQUÍ ---
        # Como no has importado Reservation, ponemos 0 para que no falle.
        # Cuando tengas el modelo Reservation importado, descomentas lo de abajo.
        # 
        booking= 0 
        
        # CODIGO PENDIENTE (Descomentar cuando importes Reservation):
        # reservations_count = Reservation.objects.filter(
        #    items__publication__owner=user,
        #    status__in=['PENDIENTE', 'CONFIRMADA', 'EN_CURSO']
        # ).distinct().count()
        # -----------------------

        data = {
            "company_name": f"{user.first_name} {user.last_name}", 
            "email": user.email,
            "phone": getattr(user, 'phone_number', 'No registrado'), 
            "location": getattr(user, 'address', 'No registrada'),   
            "published_equipments": equipment_count,
            "active_reservations": booking
        }
        
        serializer = ProviderHomeStatsSerializer(data)
        return Response(serializer.data)
    
class CategoryViewSet(viewsets.ReadOnlyModelViewSet): 
    queryset = Category.objects.all()
    serializer_class = CategorySerializer