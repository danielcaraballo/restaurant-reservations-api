from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    # Incluimos el serializador del usuario para manejar campos relacionados
    username = serializers.CharField(source="user.username", required=True, validators=[
                                     UniqueValidator(queryset=User.objects.all())])
    email = serializers.EmailField(source="user.email", required=True, validators=[
                                   UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True, source="user.password")

    class Meta:
        model = Customer
        fields = ['id', 'username', 'email', 'password', 'phone']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Extraemos los datos del usuario
        user_data = validated_data.pop('user')
        password = user_data.pop('password')
        # Creamos el usuario
        user = User.objects.create(**user_data)
        user.set_password(password)
        user.save()
        # Creamos el cliente asociado al usuario
        customer = Customer.objects.create(user=user, **validated_data)
        return customer
