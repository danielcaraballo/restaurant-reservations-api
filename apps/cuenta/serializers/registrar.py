
from rest_framework                     import serializers
from apps.cuenta.models                 import User

from rest_framework.validators import UniqueTogetherValidator
from rest_framework.response                    import Response
from rest_framework                             import status, views

class RegistrarSerializer(serializers.ModelSerializer):
    password    = serializers.CharField(write_only  = True)
    default_error_messages  = {'username': 'El nombre de usuario solo puede tener caracteres alfanumericos'}

    username            = serializers.CharField()

    def validate_username(self, value):
        username = value.lower()
        if User.objects.filter(username__iexact=username).exists():
            raise serializers.ValidationError("Nombre de usuario no disponible")
        return username
    
    class Meta:
        model   = User
        fields  = ['email', 'username', 'origen', 'cedula', 'nombre_apellido', 'password']
        extra_kwargs = {"username": {"error_messages": {"required": "Escoja un nombre de usuario"}}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)