from rest_framework import serializers
from apps.reservations.models import Area, Reservation, Table,  TableSchedule, Turn
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
                  'turn_id', 'area_id', 'table_schedule_id', 'date']
        read_only_fields = ['customer']

    def validate(self, data):
        """
        Validar datos antes de la creación de la reserva.
        """
        # Validar área activa
        try:
            area = Area.objects.get(id=data['area_id'], status=True)
        except Area.DoesNotExist:
            raise serializers.ValidationError(
                {"area": "Invalid or inactive area selected."})

        # Validar turno existente
        try:
            turn = Turn.objects.get(id=data['turn_id'])
        except Turn.DoesNotExist:
            raise serializers.ValidationError(
                {"turn": "Invalid turn selected."})

        # Validar que exista al menos una mesa disponible
        table_exists = Table.objects.filter(
            area=area,
            capacity__gte=data['number_guests'],
            status='available'
        ).exclude(
            id__in=Reservation.objects.filter(
                table_schedule__date=data['date'],
                table_schedule__turn=turn,
                status__in=['confirmed', 'pending']
            ).values_list('table_schedule__table_id', flat=True)
        ).exists()

        if not table_exists:
            raise serializers.ValidationError(
                {"table": "No available tables for the selected date, turn, and number of guests."}
            )

        return data

    def create(self, validated_data):
        """
        Crear reserva después de validar datos.
        """
        user = self.context['request'].user
        number_guests = validated_data['number_guests']
        area_id = validated_data['area_id']
        turn_id = validated_data['turn_id']
        reservation_date = validated_data['date']

        # Obtener área, turno y mesa disponible
        area = Area.objects.get(id=area_id, status=True)
        turn = Turn.objects.get(id=turn_id)
        available_table = Table.objects.filter(
            area=area,
            capacity__gte=number_guests,
            status='available'
        ).exclude(
            id__in=Reservation.objects.filter(
                table_schedule__date=reservation_date,
                table_schedule__turn=turn,
                status__in=['confirmed', 'pending']
            ).values_list('table_schedule__table_id', flat=True)
        ).first()

        # Crear TableSchedule
        table_schedule = TableSchedule.objects.create(
            table=available_table,
            date=reservation_date,
            turn=turn
        )

        # Crear Reserva
        reservation = Reservation.objects.create(
            customer=user.customer,
            number_guests=number_guests,
            table_schedule=table_schedule,
            status='pending'
        )

        return reservation
