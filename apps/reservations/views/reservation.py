from rest_framework import viewsets, serializers
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from apps.reservations.models import Reservation
from apps.reservations.serializers import ReservationsSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.select_related(
        'customer', 'table_schedule__table', 'table_schedule__turn').all()
    serializer_class = ReservationsSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get all reservations (admin) or user-specific reservations.",
        responses={200: ReservationsSerializer(many=True)},
        tags=["Reservations"],
    )
    def list(self, request, *args, **kwargs):
        """Listar reservas para administradores o reservas específicas del usuario actual."""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new reservation for the authenticated user.",
        request_body=ReservationsSerializer,
        responses={201: ReservationsSerializer()},
        tags=["Reservations"],
    )
    def create(self, request, *args, **kwargs):
        """Crear una nueva reserva para el usuario autenticado."""
        return super().create(request, *args, **kwargs)

    def get_queryset(self):
        """
        Personalizar la consulta basada en el rol del usuario.
        """
        user = self.request.user
        if user.is_staff:
            # Los administradores ven todas las reservas
            return Reservation.objects.select_related(
                'customer', 'table_schedule__table', 'table_schedule__turn'
            ).all()
        # Los usuarios regulares ven solo sus reservas
        return Reservation.objects.select_related(
            'table_schedule__table', 'table_schedule__turn'
        ).filter(customer__user=user)

    def perform_create(self, serializer):
        """
        Adjuntar al usuario autenticado a la reserva durante su creación.
        """
        serializer.save(customer=self.request.user.customer)

    def perform_update(self, serializer):
        """
        Prevenir la actualización de reservas en estados específicos.
        """
        instance = self.get_object()
        if instance.status in ['cancelled', 'completed']:
            raise serializers.ValidationError(
                {"status": "Cannot modify a cancelled or completed reservation."}
            )
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        """
        Prevenir la eliminación de reservas a menos que el usuario sea administrador.
        """
        instance = self.get_object()
        if not request.user.is_staff:
            raise serializers.ValidationError(
                {"permission": "You do not have permission to delete reservations."}
            )
        return super().destroy(request, *args, **kwargs)
