from rest_framework                     import generics, status, permissions
from apps.user.serializers.salir      import SalirSerializer
from rest_framework.response            import Response
from drf_yasg.utils                             import swagger_auto_schema


from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

class SalirAPIView(APIView):
    @swagger_auto_schema(tags = ['cuenta'],)
    def post(self, request):
        token = RefreshToken(request.data.get('refresh'))
        token.blacklist()
        return Response(status=status.HTTP_204_NO_CONTENT)