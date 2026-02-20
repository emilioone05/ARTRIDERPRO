from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permite a los Propietarios editar sus cosas.
    Los Clientes solo pueden ver (SAFE_METHODS = GET, HEAD, OPTIONS).
    """
    def has_permission(self, request, view):
        # Todos los usuarios autenticados pueden entrar
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # GET lo puede hacer cualquiera (Cliente o Propietario)
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # EDITAR/BORRAR solo si eres el dueño del objeto
        # Asumimos que el modelo tiene un campo 'owner' o 'client'
        return obj.owner == request.user