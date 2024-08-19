from django.contrib.auth.decorators     import login_required

from rest_framework                     import status
from rest_framework.response            import Response
from rest_framework.decorators          import api_view

from drf_yasg.utils                    import swagger_auto_schema
from drf_yasg                          import openapi

from apps.cuenta.models                         import User as Model
from apps.cuenta.serializers.actualizar_correo  import ActualizarCorreoSerializer


@swagger_auto_schema(   
                        methods                 = ['put'],
                        operation_description   = "Actualizar correo del usuario",
                        responses               =   {
                                                        status.HTTP_200_OK:             'Datos actualizados!',
                                                        status.HTTP_400_BAD_REQUEST:    'Datos no actualizados!'
                                                    },
                        tags                    = ['cuenta'],
                        request_body            = ActualizarCorreoSerializer
                    )
@api_view(['PUT',])
@login_required()
def actualizar_correo(request, id = None):
    model = Model.objects.filter(id = id).first()

    if model:

        if request.method == 'PUT':
            serializer = ActualizarCorreoSerializer(model, data = request.data)

            if serializer.is_valid():
                serializer.save()
                return Response({'message':'Datos actualizados!'}, status = status.HTTP_200_OK)
            return Response({'message': serializer.errors}, status = status.HTTP_400_BAD_REQUEST)
    
    return Response({'message':'Error de Operación!'}, status = status.HTTP_400_BAD_REQUEST)