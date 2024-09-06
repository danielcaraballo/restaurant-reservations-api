from rest_framework                     import generics, status
from apps.user.serializers.confirmar_reinicio_clave import ConfirmarReinicioClaveSerializer
from rest_framework.response            import Response
from apps.user.models                 import User
from django.contrib.auth.tokens         import PasswordResetTokenGenerator
from django.utils.encoding              import smart_str, DjangoUnicodeDecodeError
from django.utils.http                  import urlsafe_base64_decode
from django.http                        import HttpResponsePermanentRedirect
import os
from drf_yasg.utils                     import swagger_auto_schema

class CustomRedirect(HttpResponsePermanentRedirect):
    allowed_schemes = [os.environ.get('APP_SCHEME'), 'http', 'https']


class ConfirmarReinicioClave(generics.GenericAPIView):
    serializer_class = ConfirmarReinicioClaveSerializer
    ## URL de redireccion = http://localhost:8000/recuperar-clave/P!/P2/
    @swagger_auto_schema(tags = ['recuperación mediante correo'],)
    def get(self, request, uidb64, token):
        redirect_url = request.GET.get('redirect_url')

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id = id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                if len(redirect_url) > 3:
                    return CustomRedirect(redirect_url+'?token_valid=False')
                else:
                    return CustomRedirect(os.environ.get('FRONTEND_URL', '')+'?token_valid=False')

            if redirect_url and len(redirect_url) > 3:
                return CustomRedirect(redirect_url+'?token_valid=True&message=Credentials Valid&uidb64='+uidb64+'&token='+token)
            else:
                return CustomRedirect(os.environ.get('FRONTEND_URL', '')+'?token_valid=False')

        except DjangoUnicodeDecodeError as identifier:
            try:
                if not PasswordResetTokenGenerator().check_token(user):
                    return CustomRedirect(redirect_url+'?token_valid=False')
                    
            except UnboundLocalError as e:
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_400_BAD_REQUEST)