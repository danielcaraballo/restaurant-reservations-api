from django.db import models
from .customer import Customer
from .area import Area
from .table import TableAvailability
from .turn import Turn

STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('confirmed', 'Confirmed'),
    ('cancelled', 'Cancelled'),
]

class Reservation(models.Model):

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    number_guests = models.IntegerField('Number of guests', blank=True)
    status = models.CharField('Status', max_length=50, choices=STATUS_CHOICES, default='pending')
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    reservation_date = models.ForeignKey(TableAvailability, on_delete=models.CASCADE)
    reservation_turn = models.ForeignKey(Turn, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'reservations_reservation'
        verbose_name = 'Reservation'
        verbose_name_plural = 'Reservations'

    def __str__(self):
        return f'Reservation by {self.customer} on {self.reservation_date} at {self.reservation_turn}'
