from rest_framework import serializers
from apps.reservations.models import Table, TableSchedule


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = '__all__'


class TableScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableSchedule
        fields = '__all__'
