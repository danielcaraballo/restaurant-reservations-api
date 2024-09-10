from rest_framework                                 import status
from rest_framework.response                        import Response
from rest_framework.decorators                      import api_view

from drf_yasg.utils                                 import swagger_auto_schema
from drf_yasg                                       import openapi

from apps.user.models                             import User as Model

from apps.nomina.models.personal                    import Personal     as PersonalModel
from apps.nomina.serializers.datos_trabajador       import Serializer   as DatosTrabajadorSerializer

from apps.user.serializers. verificar_usuario     import VerificarUsuarioSerializer


@swagger_auto_schema(   
                        methods                 = ['post'],
                        operation_description   = "Verificar los datos de un usuario",
                        #manual_parameters      = [openapi.Parameter('username', openapi.IN_QUERY, "username", type = openapi.TYPE_STRING),],
                        responses               =   {
                                                        status.HTTP_200_OK:             'Existe el usuario!',
                                                        status.HTTP_400_BAD_REQUEST:    'No existe el usuario!'
                                                    },
                        tags                    = ['cuenta'],
                        request_body            = VerificarUsuarioSerializer
                    )
@api_view(['POST'])
def verificar_usuario(request,):
    verificacion    = request.data.get('verificacion', '')
    model           = Model.objects.filter(verificacion = verificacion).values('origen','cedula').first()
    
    if model:
        origen_nomina   = model["origen"]
        cedula_nomina   = model["cedula"]
        model_nomina    = PersonalModel.objects.filter(origen = origen_nomina, cedula = cedula_nomina,).values('origen','cedula','nombres_apellidos','clasificacion','cargo','dependencia','funcion','otra_funcion','entidad','numero_cuenta','anhio','estatus').first()

        if model_nomina:
            serializer = DatosTrabajadorSerializer(model_nomina)
            return Response(serializer.data, status = status.HTTP_200_OK)

    return Response({'message': 'No se encontraron datos'}, status = status.HTTP_404_NOT_FOUND)