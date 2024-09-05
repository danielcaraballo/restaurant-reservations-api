from django.db import models
from apps.reservations.models.area import Area
from apps.reservations.models.turn import Turn


class Table(models.Model):

    table_number = models.IntegerField('Table number', null=False)
    capacity = models.IntegerField('Capacity', null=False)
    area = models.ForeignKey(Area, related_name='Area', on_delete=models.PROTECT)
    status = models.BooleanField('Status', default=True, null=False)

    class Meta:
        managed = True
        db_table = 'reservations_table'
        verbose_name = 'Table'
        verbose_name_plural = 'Tables'

    def __str__(self):
        return f'{self.table_number}'


class TableAvailability(models.Model):

    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.BooleanField('Status', default=True)
    turn = models.ForeignKey(Turn, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'reservations_table_availability'
        verbose_name = 'Table Availability'
        verbose_name_plural = 'Availability of Tables'

    def __str__(self):
        return f'Table {self.table.table_number} - {self.date} - Turn: {self.turn}'
