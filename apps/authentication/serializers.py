from rest_framework import serializers
from django.contrib.auth.models import User
from apps.customers.models import Customer
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = Customer
        fields = ['username', 'email', 'password', 'phone']

    def validate_email(self, value):
        # Verifica que el email sea válido
        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError("Invalid email format.")
        return value

    def validate_password(self, value):
        # Validación de fortaleza de la contraseña
        if len(value) < 8:
            raise serializers.ValidationError(
                "Password must be at least 8 characters long.")
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError(
                "Password must contain at least one digit.")
        if not any(char.isalpha() for char in value):
            raise serializers.ValidationError(
                "Password must contain at least one letter.")
        return value

    def validate_username(self, value):
        # Comprueba que el nombre de usuario no esté duplicado
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "This username is already in use.")
        return value

    def create(self, validated_data):
        user_data = {
            'username': validated_data['username'],
            'email': validated_data['email'],
            'password': validated_data['password'],
        }
        # Crear usuario
        user = User.objects.create_user(**user_data)
        # Crear cliente asociado
        customer = Customer.objects.create(
            user=user, phone=validated_data.get('phone')
        )
        return customer
