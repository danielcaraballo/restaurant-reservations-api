from rest_framework                     import status
from rest_framework.response            import Response
from rest_framework.decorators          import api_view

from drf_yasg.utils                    import swagger_auto_schema

from apps.user.models                 import User as Model
from apps.user.serializers.responder_preguntas_recuperacion   import ResponderPreguntasRecuperacionSerializer

@swagger_auto_schema(   
                        methods                 = ['post'],
                        operation_description   = "Responder pregunstas de seguridad",
                        responses               =   {
                                                        status.HTTP_200_OK:             'Datos encontrados!',
                                                        status.HTTP_400_BAD_REQUEST:    'No se actualizaron los datos!'
                                                    },
                        tags                    = ['recuperación mediante preguntas y respuestas'],
                        request_body            = ResponderPreguntasRecuperacionSerializer
                    )
@api_view(['POST',])
def responder_preguntas_recuperacion(request,):
    email           = request.data.get('email', '')
    respuesta_01    = request.data.get('respuesta_01', '')
    respuesta_02    = request.data.get('respuesta_02', '')
    respuesta_03    = request.data.get('respuesta_03', '')

    model = Model.objects.filter(email = email).filter(respuesta_01 = respuesta_01).filter(respuesta_02 = respuesta_02).filter(respuesta_03 = respuesta_03).first()
    if model:
        return Response({'message':'Respondiste bien!'},status = status.HTTP_200_OK)
    
    return Response({'message':'Respondiste mal!'}, status = status.HTTP_400_BAD_REQUEST)