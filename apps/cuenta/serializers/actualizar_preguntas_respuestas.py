from rest_framework                         import serializers
from apps.cuenta.models                     import User as Model


class ActualizarPreguntasRespuestasSerializer(serializers. ModelSerializer):
    class Meta:
        model   = Model
        fields  =   (
                    'pregunta_01',
                    'pregunta_02',
                    'pregunta_03',
                    'respuesta_01',
                    'respuesta_02',
                    'respuesta_03',
                    )
        extra_kwargs    =   {
                                'pregunta_01':      {'required': True},
                                'pregunta_02':      {'required': True},
                                'pregunta_03':      {'required': True},
                                'respuesta_01':     {'required': True},
                                'respuesta_02':     {'required': True},
                                'respuesta_03':     {'required': True},
                            }