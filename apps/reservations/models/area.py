from django.db import models


class Area(models.Model):

    name = models.CharField('Name', max_length=30, null=False)
    status = models.BooleanField('Status', null=False)

    class Meta:
        managed = True
        db_table = 'reservations_area'
        verbose_name = 'Area'
        verbose_name_plural = 'Areas'

    def __str__(self):
        return f'{self.name}'
