from django.db.models import Q
from rest_framework import serializers
from apps.reservations.models import Reservation, Turn, Table, Area, TableSchedule
from apps.customers.serializers import CustomerSerializer


class ReservationsSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    number_guests = serializers.IntegerField(write_only=True)
    turn_id = serializers.IntegerField(write_only=True)
    area_id = serializers.IntegerField(write_only=True)
    date = serializers.DateField(write_only=True)

    class Meta:
        model = Reservation
        fields = ['id', 'customer', 'number_guests',
                  'turn_id', 'table_schedule_id', 'date', 'area_id']
        read_only_fields = ['customer']

    def create(self, validated_data):
        user = self.context['request'].user
        number_guests = validated_data.pop('number_guests')
        area_id = validated_data.pop('area_id')
        turn_id = validated_data.pop('turn_id')
        reservation_date = validated_data.pop('date')

        # Verificar que el área existe y está activa
        try:
            area = Area.objects.get(id=area_id, status=True)
        except Area.DoesNotExist:
            raise serializers.ValidationError(
                "Invalid or inactive area selected.")

        # Verificar que el turno existe
        try:
            turn = Turn.objects.get(id=turn_id)
        except Turn.DoesNotExist:
            raise serializers.ValidationError("Invalid turn selected.")

        # Buscar mesas disponibles
        available_table = Table.objects.filter(
            area=area,
            capacity__gte=number_guests,
            status='available',
        ).exclude(
            id__in=Reservation.objects.filter(
                table_schedule__date=reservation_date,
                table_schedule__turn=turn,
                status__in=['confirmed', 'pending']
            ).values_list('table_schedule__table_id', flat=True)
        ).first()

        if not available_table:
            raise serializers.ValidationError(
                "No available tables for the selected date, turn, and number of guests."
            )

        # Crear el registro en TableSchedule
        table_schedule = TableSchedule.objects.create(
            table=available_table,
            date=reservation_date,
            turn=turn
        )

        # Crear la reserva con estado pendiente
        reservation = Reservation.objects.create(
            customer=user.customer,
            number_guests=number_guests,
            table_schedule=table_schedule,
            status='pending'
        )

        return reservation
