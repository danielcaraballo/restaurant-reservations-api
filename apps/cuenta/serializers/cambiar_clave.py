from rest_framework                         import serializers
from apps.cuenta.models                     import User as Model


class CambiarClaveSerializer(serializers.Serializer):
    model           = Model
    old_password    = serializers.CharField(required=True)
    new_password    = serializers.CharField(required=True)