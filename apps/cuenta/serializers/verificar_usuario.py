from rest_framework                         import serializers

from apps.cuenta.models                     import User as Model


class VerificarUsuarioSerializer(serializers. ModelSerializer):
    class Meta:
        model   = Model
        fields  =   (
                        'verificacion',
                    )