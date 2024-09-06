from rest_framework                             import status, views
from apps.user.serializers.verificar_correo   import VerificarCorreoSerializer
from rest_framework.response                    import Response
from apps.user.models                         import User
import jwt
from django.conf                                import settings
from drf_yasg.utils                             import swagger_auto_schema
from drf_yasg                                   import openapi
from django.shortcuts                           import render


class VerificarCorreo(views.APIView):
    serializer_class    = VerificarCorreoSerializer

    token_param_config  = openapi.Parameter('token', in_ = openapi.IN_QUERY, description = 'Description', type = openapi.TYPE_STRING)
    
    @swagger_auto_schema(tags = ['Creación de cuenta'], manual_parameters = [token_param_config])
    def get(self, request):
        token = request.GET.get('token')

        try:
            print('hola')
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            print(payload)
            user    = User.objects.get(id = payload['user_id'])
            print(user)

            if not user.is_verified:
                user.is_verified = True
                user.save()
            #return Response({'email': 'Se ha activado exitosamente'}, status = status.HTTP_200_OK)
            return render(request, 'frontend/cuenta_verificada.html')
        
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activacion Expirada'}, status = status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Token Invalido'}, status = status.HTTP_400_BAD_REQUEST)