from django.db import models


class AreaStatus(models.TextChoices):
    ACTIVE = 'active', 'Active'
    INACTIVE = 'inactive', 'Inactive'


class Area(models.Model):

    name = models.CharField('Name', max_length=30, null=False)
    status = models.CharField(
        'Status', max_length=20, choices=AreaStatus.choices, default=AreaStatus.ACTIVE)

    class Meta:
        managed = True
        db_table = 'reservations_area'
        verbose_name = 'Area'
        verbose_name_plural = 'Areas'

    def __str__(self):
        return f'{self.name}'
