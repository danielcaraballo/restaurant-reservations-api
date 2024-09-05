
from rest_framework                         import status
from rest_framework                         import generics
from rest_framework.response                import Response
from rest_framework.permissions             import IsAuthenticated
from apps.user.models                     import User as Model
from apps.user.serializers.cambiar_clave  import CambiarClaveSerializer
from drf_yasg.utils                             import swagger_auto_schema

class CambiarClave(generics. UpdateAPIView):

    serializer_class    = CambiarClaveSerializer
    model               = Model
    permission_classes  = (IsAuthenticated,)

    @swagger_auto_schema(tags = ['seguridad'],)
    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    @swagger_auto_schema(tags = ['Seguridad'],)
    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer  = self.get_serializer(data = request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Clave erronea."]}, status=status.HTTP_400_BAD_REQUEST)

            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                            'status': 'success',
                            'code': status.HTTP_200_OK,
                            'message': 'la clave se ha actualizado!',
                            #'data': []
                        }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)