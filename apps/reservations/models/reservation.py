from django.db import models
from django.core.exceptions import ValidationError
from datetime import date
from .table import TableSchedule
from apps.customers.models import Customer


class ReservationStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    CONFIRMED = 'confirmed', 'Confirmed'
    CANCELLED = 'cancelled', 'Cancelled'
    COMPLETED = 'completed', 'Completed'


class Reservation(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name='reservations')
    number_guests = models.PositiveIntegerField(
        'Number of guests', blank=True, null=True)
    status = models.CharField(
        'Status', max_length=20, choices=ReservationStatus.choices, default=ReservationStatus.PENDING)
    table_schedule = models.ForeignKey(TableSchedule, on_delete=models.PROTECT)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'reservations_reservation'
        verbose_name = 'Reservation'
        verbose_name_plural = 'Reservations'

    def clean(self):
        # Validar que el número de invitados no sea negativo
        if self.number_guests < 0:
            raise ValidationError('Number of guests cannot be negative.')

        # Validar que la capacidad de la mesa sea suficiente
        if self.table_schedule.table.capacity < self.number_guests:
            raise ValidationError(
                "The number of guests exceeds the table capacity.")

        # Validar que la reserva no esté en el pasado
        if self.table_schedule.date < date.today():
            raise ValidationError(
                "The reservation date cannot be in the past.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Reservation for {self.customer} on {self.table_schedule.date} at {self.table_schedule.turn}'
