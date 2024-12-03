from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from apps.reservations.models import Table, TableSchedule
from apps.reservations.serializers import TableSerializer, TableScheduleSerializer


class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    permission_classes = [IsAdminUser]


class TableScheduleViewSet(viewsets.ModelViewSet):
    queryset = TableSchedule.objects.all()
    serializer_class = TableScheduleSerializer
    permission_classes = [IsAdminUser]
