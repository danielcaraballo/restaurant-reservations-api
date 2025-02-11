from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from .serializers import RegisterSerializer


class LoginView(APIView):
    permission_classes = []

    def post(self, request):
        identifier = request.data.get('identifier')
        password = request.data.get('password')

        if not identifier or not password:
            return Response({'error': 'Username/Email and Password are required'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=identifier, password=password)
        if user:
            if not user.is_active:
                return Response({'error': 'Inactive account'}, status=status.HTTP_403_FORBIDDEN)

            refresh = RefreshToken.for_user(user)
            role = 'admin' if user.is_staff else 'customer'

            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'role': role,
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            customer = serializer.save()
            refresh = RefreshToken.for_user(
                customer.user)
            return Response({
                'customer': serializer.data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    def post(self, request):
        # Extraer el refresh token
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response(
                {'detail': 'Refresh token is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Intentar revocar el token
            token = RefreshToken(refresh_token)

            # Blacklist del token si el soporte está habilitado
            if hasattr(token, 'blacklist'):
                token.blacklist()
                return Response(
                    {'detail': 'Logout successful.'},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'detail': 'Token blacklist support is not enabled on this server.'},
                    status=status.HTTP_501_NOT_IMPLEMENTED
                )

        except TokenError as e:
            # Error específico del token (token inválido, expirado, etc.)
            return Response(
                {'detail': f'Invalid token: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            # Excepción genérica para errores no previstos
            return Response(
                {'detail': f'An unexpected error occurred: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
