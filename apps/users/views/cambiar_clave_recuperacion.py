from rest_framework                     import status
from rest_framework                     import generics
from rest_framework.response            import Response
from rest_framework.decorators          import api_view

from drf_yasg.utils                    import swagger_auto_schema

from apps.user.models                 import User as Model

from apps.user.serializers.cambiar_clave_recuperacion     import CambiarClaveRecuperacionSerializer


@swagger_auto_schema(   
                        methods                 = ['post'],
                        operation_description   = "Cambiar clave de usuario trasresponder las preguntas correctamente",
                        responses               =   {
                                                        status.HTTP_200_OK:             'Recuperada!',
                                                        status.HTTP_400_BAD_REQUEST:    'Error en la opración!'
                                                    },
                        tags                    = ['recuperación mediante preguntas y respuestas'],
                        request_body            = CambiarClaveRecuperacionSerializer
                    )
@api_view(['POST'])
def cambiar_clave_recuperacion(request,):
    email        = request.data.get('email', '')
    model = Model.objects.filter(email = email).first()
    
    if model:
        password = request.data.get('password', '')
        user = Model.objects.get(email = email)
        user.set_password(password)
        user.save()
        return Response({'message':'¡Se ha recuperado la clave!'}, status = status.HTTP_200_OK)
    return Response({'message':'Error en la operación!'}, status = status.HTTP_400_BAD_REQUEST)