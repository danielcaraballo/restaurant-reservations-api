from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from apps.reservations.models import Reservation
from apps.reservations.serializers import ReservationsSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationsSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get all reservations (admin) or user-specific reservations.",
        responses={200: ReservationsSerializer(many=True)},
        tags=["Reservations"],
    )
    def list(self, request, *args, **kwargs):
        """Override if needed for documentation."""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new reservation for the authenticated user.",
        request_body=ReservationsSerializer,
        responses={201: ReservationsSerializer()},
        tags=["Reservations"],
    )
    def create(self, request, *args, **kwargs):
        """Override to customize."""
        return super().create(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Reservation.objects.all()
        return Reservation.objects.filter(customer__user=user)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user.customer)

    def perform_update(self, serializer):
        instance = self.get_object()
        if instance.status in ['cancelled', 'completed']:
            raise serializers.ValidationError(
                "Cannot modify a cancelled or completed reservation.")
        serializer.save()
