from rest_framework                         import serializers
from apps.user.models                     import User as Model


class ResponderPreguntasRecuperacionSerializer(serializers. ModelSerializer):
    class Meta:
        model   = Model
        fields  = (
                    'email',
                    'respuesta_01',
                    'respuesta_02',
                    'respuesta_03',
                    )