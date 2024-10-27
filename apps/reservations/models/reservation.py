from django.db import models
from django.core.exceptions import ValidationError
from .area import Area
from .table import TableAvailability
from .turn import Turn
from apps.customers.models import Customer


STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('confirmed', 'Confirmed'),
    ('cancelled', 'Cancelled'),
]


class Reservation(models.Model):

    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name='reservations')
    number_guests = models.IntegerField('Number of guests', blank=True)
    status = models.CharField('Status', max_length=50,
                              choices=STATUS_CHOICES, default='pending')
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    reservation_date = models.ForeignKey(
        TableAvailability, on_delete=models.CASCADE)
    reservation_turn = models.ForeignKey(Turn, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'reservations_reservation'
        verbose_name = 'Reservation'
        verbose_name_plural = 'Reservations'

    def clean(self):
        if self.number_guests < 0:
            raise ValidationError('Number of guests cannot be negative.')

    def clean(self):
        if Reservation.objects.filter(reservation_date=self.reservation_date, reservation_turn=self.reservation_turn).exists():
            raise ValidationError(
                'The table is already reserved for this date and time.')

    def __str__(self):
        return f'Reservation for {self.customer} on {self.reservation_date} at {self.reservation_turn}'
