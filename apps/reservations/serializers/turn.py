from rest_framework import serializers
from apps.reservations.models import Turn


class TurnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turn
        fields = '__all__'

    def validate(self, data):
        if data['opening_time'] >= data['closing_time']:
            raise serializers.ValidationError(
                'Opening time must be before closing time.')
        return data
