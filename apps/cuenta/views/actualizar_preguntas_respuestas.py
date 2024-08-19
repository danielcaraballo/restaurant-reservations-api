from django.contrib.auth.decorators     import login_required

from rest_framework                     import status
from rest_framework.response            import Response
from rest_framework.decorators          import api_view
from drf_yasg.utils                     import swagger_auto_schema
from drf_yasg                           import openapi
from apps.cuenta.models                 import User as Model
from apps.cuenta.serializers.actualizar_preguntas_respuestas    import ActualizarPreguntasRespuestasSerializer


@swagger_auto_schema(   
                        methods                 = ['put'],
                        operation_description   = "Actualizar datos de la cuenta",
                        #manual_parameters      = [openapi.Parameter('ID', openapi.IN_QUERY, "id", type = openapi.TYPE_STRING),], 
                        responses               =   {
                                                        status.HTTP_200_OK:             'Datos actualizados!',
                                                        status.HTTP_400_BAD_REQUEST:    'No se actualizaron los datos!'
                                                    },
                        tags                    = ['cuenta'],
                        request_body            = ActualizarPreguntasRespuestasSerializer
                    )
@api_view(['PUT',])
@login_required(login_url = "/cuenta/entrar/")
def actualizar_preguntas_respuestas_recuperacion(request, id = None):
    model = Model.objects.filter(id = id).first()

    if model:

        if request.method == 'PUT':
            serializer = ActualizarPreguntasRespuestasSerializer(model, data = request.data)

            if serializer.is_valid():
                serializer.save()
                return Response({'message':'Datos actualizados!'}, status = status.HTTP_200_OK)
            return Response({'message': serializer.errors}, status = status.HTTP_400_BAD_REQUEST)
    
    return Response({'message':'No se actualizaron los datos!'}, status = status.HTTP_400_BAD_REQUEST)