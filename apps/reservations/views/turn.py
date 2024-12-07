from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from apps.reservations.models import Turn
from apps.reservations.serializers import TurnSerializer


class TurnViewSet(viewsets.ModelViewSet):
    queryset = Turn.objects.all()
    serializer_class = TurnSerializer
    permission_classes = [IsAdminUser]
