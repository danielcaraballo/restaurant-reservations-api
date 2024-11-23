from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .models import Customer
from .serializers import CustomerSerializer


# Permiso personalizado para distinguir roles
class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class IsCustomerUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and hasattr(request.user, 'customer')


# Vista para listar y crear clientes (solo para administradores)
class CustomerListCreateView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


# Vista para obtener, actualizar o eliminar detalles de cliente
class CustomerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.user.is_staff:
            return [IsAdminUser()]
        return [IsCustomerUser()]

    # Filtra para que los clientes solo puedan acceder a sus propios datos
    def get_queryset(self):
        if self.request.user.is_staff:
            return super().get_queryset()
        return Customer.objects.filter(user=self.request.user)


# Vista de registro para clientes
class CustomerRegisterView(generics.CreateAPIView):
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        customer = serializer.save()

        # Genera los tokens JWT
        refresh = RefreshToken.for_user(customer.user)

        return Response({
            'customer': serializer.data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
