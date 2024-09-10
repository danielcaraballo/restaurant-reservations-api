from rest_framework                         import serializers

from apps.user.models                     import User as Model


class BuscarPreguntasRecuperacionSerializer(serializers. ModelSerializer):
    class Meta:
        model   = Model
        fields  =   (
                        'email',
                    )
        extra_kwargs    =   {
                                'email':      {'required': True},
                            }