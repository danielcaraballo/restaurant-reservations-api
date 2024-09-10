from rest_framework                         import serializers

from apps.nomina.models.trabajador          import Trabajador as Model


class ComprobarExistenciaUsuarioSerializer(serializers. ModelSerializer):
    class Meta:
        model   = Model
        fields  =   (
                        'origen',
                        'cedula',
                        'cuenta_bancaria',
                    )