from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from apps.reservations.models import (Area, Rating, Reservation,
                                      Restaurant, Table, TableSchedule, Turn)
from apps.reservations.serializers import (AreaSerializer, RatingSerializer,
                                           ReservationsSerializer, RestaurantSerializer,
                                           TableSerializer, TableScheduleSerializer, TurnSerializer)
from apps.customers.models import Customer
from apps.customers.serializers import CustomerSerializer


class AreaViewSet(viewsets.ModelViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer


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


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer


class TableScheduleViewSet(viewsets.ModelViewSet):
    queryset = TableSchedule.objects.all()
    serializer_class = TableScheduleSerializer


class TurnViewSet(viewsets.ModelViewSet):
    queryset = Turn.objects.all()
    serializer_class = TurnSerializer
