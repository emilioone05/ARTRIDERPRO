from django.urls import path, include
from rest_framework.routers import DefaultRouter
# IMPORTAMOS LA VISTA CON EL NOMBRE CORREGIDO
from .views import (
    PublicationViewSet, 
    UnitViewSet, 
    PackageViewSet,
    ProviderCatalogView,  
    ProviderHomeView,
    CategoryViewSet
)

router = DefaultRouter()
router.register(r'publicaciones', PublicationViewSet, basename='publication')
router.register(r'units', UnitViewSet, basename='unit')
router.register(r'packages', PackageViewSet, basename='package')
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    # Rutas automáticas del router
    path('', include(router.urls)), 

    path('provider/catalog/', ProviderCatalogView.as_view(), name='provider-catalog'),
    
    path('provider/home/', ProviderHomeView.as_view(), name='provider-home'),
]