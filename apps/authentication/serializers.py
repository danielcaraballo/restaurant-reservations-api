from rest_framework import serializers
from django.contrib.auth.models import User
from apps.customers.models import Customer
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
import random
import string

User = get_user_model()


def generate_username(email):
    """Generar un nombre de usuario único basado en el email"""
    base_username = email.split(
        '@')[0]  # Usamos la parte antes del '@' del correo
    username = base_username

    # Aseguramos que el nombre de usuario sea único
    while User.objects.filter(username=username).exists():
        username = base_username + ''.join(random.choices(string.digits, k=4))

    return username


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, source='user.email')
    password = serializers.CharField(
        write_only=True, min_length=8, source='user.password')
    password_confirmation = serializers.CharField(
        write_only=True, min_length=8, source='user.password_confirmation')
    first_name = serializers.CharField(required=True, source='user.first_name')
    last_name = serializers.CharField(required=True, source='user.last_name')
    phone = serializers.CharField(required=True)

    class Meta:
        model = Customer
        fields = ['email', 'password', 'password_confirmation',
                  'first_name', 'last_name', 'phone']

    def validate_email(self, value):
        # Verifica que el email sea válido
        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError("Invalid email format.")
        # Verifica que el email no esté duplicado
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
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

    def validate(self, data):
        # Asegurarse de que las contraseñas coincidan
        if data['user']['password'] != data['user']['password_confirmation']:
            raise serializers.ValidationError(
                "The passwords must match.")
        return data

    def create(self, validated_data):
        """Crea un usuario y un cliente asociado con username automático"""

        # Extraer datos relacionados con el modelo User
        user_data = validated_data.pop('user')

        # Eliminar password_confirmation
        user_data.pop('password_confirmation', None)

        # Generar username automático
        username = generate_username(user_data['email'])
        user_data['username'] = username

        # Crear el usuario
        user = User.objects.create_user(**user_data)

        # Crear el cliente asociado al usuario
        customer = Customer.objects.create(user=user, **validated_data)
        return customer
