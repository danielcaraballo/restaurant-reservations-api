from rest_framework                     import generics, status
from apps.user.serializers.solicitar_reinicio_clave import SoliciarReinicioClaveSerializer
from rest_framework.response            import Response
from apps.user.models                 import User
from apps.user.utils                  import Util
from django.contrib.sites.shortcuts     import get_current_site
from django.urls                        import reverse
from django.contrib.auth.tokens         import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts     import get_current_site
from django.utils.http                  import urlsafe_base64_encode
from django.utils.encoding              import smart_bytes
from django.urls                        import reverse

from drf_yasg.utils                     import swagger_auto_schema

from apps.user.utils                  import Util


class SoliciarReinicioClave(generics.GenericAPIView):
    serializer_class = SoliciarReinicioClaveSerializer

    @swagger_auto_schema(tags = ['recuperación mediante correo'],)
    def post(self, request):
        serializer  = self.serializer_class(data = request.data)
        email       = request.data.get('email', '')

        if User.objects.filter(email = email).exists():
            user            = User.objects.get(email = email)
            uidb64          = urlsafe_base64_encode(smart_bytes(user.id))
            token           = PasswordResetTokenGenerator().make_token(user)
            current_site    = get_current_site(request = request).domain
            relativeLink    = reverse('reiniciar-clave', kwargs={'uidb64': uidb64, 'token': token})
            redirect_url    = request.data.get('redirect_url', '')
            absurl          = 'http://'+current_site + relativeLink
            email_body      = 'Saludos, \n puedes usar el siguiente link para reiniciar tu clave  \n' + absurl + "?redirect_url=" + redirect_url + "/" + uidb64 + "/" + token + "/"  
            data            = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'Reiniciar su clave'}
            Util.send_email(data)
        return Response({'message': 'Le hemos enviado un link para reiniciar su clave'}, status = status.HTTP_200_OK)