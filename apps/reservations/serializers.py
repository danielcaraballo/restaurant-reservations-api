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

    def validate_email(self, value):
        if Customer.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email is already in use.')
        return value


class RatingSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)

    class Meta:
        model = Rating
        fields = '__all__'

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError(
                'Rating must be between 1 and 5.')
        return value


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'


class TurnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turn
        fields = '__all__'

    def validate(self, data):
        if data['opening_time'] >= data['closing_time']:
            raise serializers.ValidationError(
                'Opening time must be before closing time.')
        return data


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


class ReservationsSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    area = AreaSerializer(read_only=True)
    reservation_date = TableAvailabilitySerializer(read_only=True)
    reservation_turn = TurnSerializer(read_only=True)

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
