from rest_framework import serializers
from .turn import TurnSerializer
from apps.reservations.models import Table, TableAvailability


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = '__all__'


class TableAvailabilitySerializer(serializers.ModelSerializer):
    table = TableSerializer(read_only=True)
    turn = TurnSerializer(read_only=True)

    class Meta:
        model = TableAvailability
        fields = '__all__'

    def validate(self, data):
        if TableAvailability.objects.filter(
            table=data['table'],
            date=data['date'],
            turn=data['turn']
        ).exists():
            raise serializers.ValidationError(
                'The table is already available for this date and time.')
        return data
