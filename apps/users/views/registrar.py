from rest_framework                     import generics, status
from apps.user.serializers.registrar  import RegistrarSerializer
from rest_framework.response            import Response
from rest_framework_simplejwt.tokens    import RefreshToken
from apps.user.models                 import User
from apps.user.utils                  import Util
from django.contrib.sites.shortcuts     import get_current_site
from django.urls                        import reverse
from apps.user.renderers              import UserRenderer
from django.contrib.sites.shortcuts     import get_current_site
from django.urls                        import reverse
from apps.user.utils                  import Util
from drf_yasg.utils                     import swagger_auto_schema

class RegistraView(generics.GenericAPIView):
    serializer_class = RegistrarSerializer
    renderer_classes = (UserRenderer,)

    @swagger_auto_schema(tags = ['Creación de cuenta'],)
    def post(self, request):
        user            = request.data
        serializer      = self.serializer_class(data = user)
        serializer.is_valid(raise_exception = True)
        serializer.save()

        user_data       = serializer.data
        '''
        user            = User.objects.get(username = user_data['username'])
        token           = RefreshToken.for_user(user).access_token
        current_site    = get_current_site(request).domain
        relativeLink    = reverse('verificar-correo')
        absurl          = 'http://'+current_site+relativeLink+"?token="+str(token)
        email_body      = 'Saludos '+user.username + ', Use el siguiente link para verificar su correol \n' + absurl
        data            = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'Revise su correo'}
        Util.send_email(data)        
        '''

        return Response(user_data, status = status.HTTP_201_CREATED)