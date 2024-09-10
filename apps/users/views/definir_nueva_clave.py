from rest_framework                     import generics, status
from apps.user.serializers.confirmar_reinicio_clave import ConfirmarReinicioClaveSerializer
from rest_framework.response            import Response
from drf_yasg.utils                     import swagger_auto_schema

class DefinirNuevaClave(generics.GenericAPIView):
    serializer_class = ConfirmarReinicioClaveSerializer

    @swagger_auto_schema(tags = ['recuperación mediante correo'],)
    def patch(self, request):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)
        return Response({'success': True, 'message': 'La clave ha sido reiniciada'}, status = status.HTTP_200_OK)


