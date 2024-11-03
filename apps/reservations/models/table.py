from django.db import models
from django.core.exceptions import ValidationError
from .area import Area
from .turn import Turn


class Table(models.Model):

    table_number = models.IntegerField('Table number', unique=True)
    capacity = models.PositiveIntegerField('Capacity', null=False)
    area = models.ForeignKey(Area, related_name='tables',
                             on_delete=models.PROTECT)
    status = models.CharField('Status', max_length=20, choices=[
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('maintenance', 'Under Maintenance')
    ], default='available')

    class Meta:
        managed = True
        db_table = 'reservations_table'
        verbose_name = 'Table'
        verbose_name_plural = 'Tables'

    def clean(self):
        if self.capacity <= 0:
            raise ValidationError("Table capacity must be greater than zero.")

    def __str__(self):
        return f'{self.table_number}'


class TableSchedule(models.Model):
    table = models.ForeignKey(
        Table, on_delete=models.CASCADE, related_name='schedules')
    date = models.DateField('Date', null=False)
    turn = models.ForeignKey(Turn, on_delete=models.CASCADE)
    is_available = models.BooleanField('Is Available', default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['table', 'date', 'turn'], name='unique_table_schedule')]
        managed = True
        db_table = 'reservations_table_schedule'
        verbose_name = 'Table schedule'
        verbose_name_plural = 'Schedule of Tables'

    def __str__(self):
        return f'Table {self.table.table_number} - {self.date} - Turn: {self.turn}'
