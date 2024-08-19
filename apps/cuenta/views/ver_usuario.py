from django.contrib.auth.decorators     import login_required

from rest_framework                     import status
from rest_framework.response            import Response
from rest_framework.decorators          import api_view

from drf_yasg.utils                    import swagger_auto_schema

from apps.cuenta.models                     import User         as Model
from apps.cuenta.serializers.datos_usuario  import Serializer   as UsuarioSerializers

@swagger_auto_schema(   
                        methods                 = ['get'],
                        operation_description   = "Ver datos del usuario",
                        responses               =   {
                                                        status.HTTP_200_OK:             'Datos encontrados!',
                                                        status.HTTP_400_BAD_REQUEST:    'Error en la operación!'
                                                    },
                        tags                    = ['cuenta'],
                    )
@api_view(['GET'])
@login_required()
def ver_usuario(request, id):
    model = Model.objects.filter(id = id).first()
    
    if model:
        serializer = UsuarioSerializers(model)
        return Response(serializer.data, status = status.HTTP_200_OK)
    return Response({'message':'Error en la operación!'}, status = status.HTTP_400_BAD_REQUEST)