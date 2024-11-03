from rest_framework import serializers
from .area import AreaSerializer
from .table import TableScheduleSerializer
from apps.reservations.models import Reservation
from apps.customers.serializers import CustomerSerializer


class ReservationsSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    area = AreaSerializer(read_only=True)
    table_schedule = TableScheduleSerializer(read_only=True)
    

    class Meta:
        model = Reservation
        fields = '__all__'

    def validate_number_guests(self, value):
        if value < 0:
            raise serializers.ValidationError(
                'Number of guests cannot be negative.')
        return value

    def validate(self, data):
        if Reservation.objects.filter(
            reservation_date=data['reservation_date'],
            reservation_turn=data['reservation_turn']
        ).exists():
            raise serializers.ValidationError(
                'The table is already reserved for this date and time.')
        return data
