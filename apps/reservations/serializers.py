from rest_framework import serializers
from .models import (Area, Customer, Rating, Reservation,
                     Restaurant, Table, TableAvailability, Turn)


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class RatingSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)

    class Meta:
        model = Rating
        fields = '__all__'


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'


class TurnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turn
        fields = '__all__'


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


class ReservationsSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    area = AreaSerializer(read_only=True)
    reservation_date = TableAvailabilitySerializer(read_only=True)
    reservation_turn = TurnSerializer(read_only=True)

    class Meta:
        model = Reservation
        fields = '__all__'
