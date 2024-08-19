from rest_framework                     import status
from rest_framework.response            import Response
from rest_framework.decorators          import api_view

from drf_yasg.utils                    import swagger_auto_schema

from apps.cuenta.models                 import User as Model

from apps.cuenta.serializers.buscar_preguntas_recuperacion  import BuscarPreguntasRecuperacionSerializer
from apps.cuenta.serializers.mostrar_preguntas_recuperacion import MostarPreguntasRecueracionSerializer

@swagger_auto_schema(   
                        methods                 = ['post'],
                        operation_description   = "Ver preguntas definidas por el usuario",
                        responses               =   {
                                                        status.HTTP_200_OK:             'Recuperada!',
                                                        status.HTTP_400_BAD_REQUEST:    'Error en la opración!'
                                                    },
                        tags                    = ['recuperación mediante preguntas y respuestas'],
                        request_body            = BuscarPreguntasRecuperacionSerializer
                    )
@api_view(['POST'])
def buscar_preguntas_recuperacion(request,):
    email = request.data.get('email', '')
    model = Model.objects.filter(email = email).first()
    
    if model:
        serializer = MostarPreguntasRecueracionSerializer(model)
        return Response(serializer.data, status = status.HTTP_200_OK)
    return Response({'message':'Correo no registrado'}, status = status.HTTP_400_BAD_REQUEST)