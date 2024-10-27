from rest_framework import serializers
from apps.reservations.models import Rating
from apps.customers.serializers import CustomerSerializer


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
