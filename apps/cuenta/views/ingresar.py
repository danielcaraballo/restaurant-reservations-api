from rest_framework                     import status
from rest_framework.response            import Response

from drf_yasg.utils                             import swagger_auto_schema

from rest_framework.exceptions          import AuthenticationFailed
from django.contrib.auth                import authenticate
from rest_framework_simplejwt.views     import TokenObtainPairView

from apps.cuenta.serializers.ingresar   import MyTokenObtainPairSerializer, LoginSerializer

class IngresarAPIView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    @swagger_auto_schema(tags = ['cuenta'],)
    def post(self, request, *args, **kwargs):
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        user     = authenticate(username = username, password = password)

        if not user:
            raise AuthenticationFailed('Credencales invalidas, intente nuevamente')
        if not user.is_active:
            raise AuthenticationFailed('Cuenta inactiva, contacte con el administrador')
        
        if not user.is_verified:
            raise AuthenticationFailed('Correo no verificado')        

        if user:
            login_serializer = self.serializer_class(data = request.data)
            if login_serializer.is_valid():
                user_serializer = LoginSerializer(user)

                return Response(
                                {
                                    'token':            login_serializer.validated_data.get('access'),
                                    'refresh_token':    login_serializer.validated_data.get('refresh'),
                                    'usuario':          user_serializer.data,
                                    #'status':           'OK',
                                    #'message':          'Atenticación exitosa'
                                },
                                status = status.HTTP_200_OK)
            return Response({'error': 'Contraseña o nombre de usuario incorrectos'}, status = status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Contraseña o nombre de usuario incorrectos'}, status = status.HTTP_400_BAD_REQUEST)