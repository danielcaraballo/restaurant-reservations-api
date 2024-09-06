from rest_framework                         import serializers

from apps.user.models                     import User as Model


class Serializer(serializers. ModelSerializer):
    class Meta:
        model   = Model
        fields  =   (
                        'verificacion',
                    )