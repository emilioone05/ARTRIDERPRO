from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PaqueteViewSet

router = DefaultRouter()
router.register(r'', PaqueteViewSet) # Ojo: cadena vacía porque el prefijo va en config

urlpatterns = [
    path('', include(router.urls)),
]