from rest_framework                         import serializers

from apps.user.models                     import User as Model

class CambiarClaveRecuperacionSerializer(serializers. ModelSerializer):
    class Meta:
        model   =   Model
        fields  =   (
                        'email',
                        'password',
                    )