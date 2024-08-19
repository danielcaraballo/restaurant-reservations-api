
from rest_framework                     import serializers
from apps.cuenta.models                 import User


class VerificarCorreoSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length = 555)

    class Meta:
        model   = User
        fields  = ['token']