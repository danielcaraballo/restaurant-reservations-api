from django.db import models
from django.core.exceptions import ValidationError


class Turn(models.Model):

    name = models.CharField('Name', max_length=50, null=False, blank=False)
    opening_time = models.TimeField()
    closing_time = models.TimeField()

    class Meta:
        managed = True
        db_table = 'reservations_turn'
        verbose_name = 'Turn'
        verbose_name_plural = 'Turns'

    def clean(self):
        if self.opening_time >= self.closing_time:
            raise ValidationError('Opening time must be before closing time.')

    def __str__(self):
        return f'{self.name}'
