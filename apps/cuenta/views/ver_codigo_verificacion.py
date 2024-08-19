from django.contrib.auth.decorators                 import login_required

from rest_framework                                 import status
from rest_framework.response                        import Response
from rest_framework.decorators                      import api_view

from drf_yasg.utils                                 import swagger_auto_schema

from apps.cuenta.models                             import User         as Model
from apps.cuenta.serializers.codigo_verificacion    import Serializer

@swagger_auto_schema(   
                        methods                 = ['get'],
                        operation_description   = "Ver código de verificación de un usuario",
                        responses               =   {
                                                        status.HTTP_200_OK:             'Datos encontrados!',
                                                        status.HTTP_400_BAD_REQUEST:    'Error en la operación!'
                                                    },
                        tags                    = ['cuenta'],
                    )
@api_view(['GET'])
@login_required()
def ver_codigo_verificacion(request, origen, cedula):
    model = Model.objects.filter(origen = origen, cedula = cedula).first()
    
    if model:
        serializer = Serializer(model)
        return Response(serializer.data, status = status.HTTP_200_OK)
    return Response({'message':'Error en la operación!'}, status = status.HTTP_400_BAD_REQUEST)