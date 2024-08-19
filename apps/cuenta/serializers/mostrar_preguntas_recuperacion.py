from rest_framework                         import serializers

from apps.cuenta.models                     import User as Model


class MostarPreguntasRecueracionSerializer(serializers. ModelSerializer):
    class Meta:
        model   = Model
        fields  = (
                    'email',
                    'pregunta_01',
                    'pregunta_02',
                    'pregunta_03',
                    )