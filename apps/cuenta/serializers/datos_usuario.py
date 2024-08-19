from rest_framework                         import serializers

from apps.cuenta.models                     import User as Model


class Serializer(serializers. ModelSerializer):
    class Meta:
        model   = Model
        fields  = (
                    'id',
                    'verificacion',
                    'username',
                    'email',
                    'origen',
                    'cedula',
                    'nombre_apellido',
                    'pregunta_01',
                    'pregunta_02',
                    'pregunta_03',
                    'respuesta_01',
                    'respuesta_02',
                    'respuesta_03'
                    )