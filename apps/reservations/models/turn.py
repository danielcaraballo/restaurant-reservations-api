from django.db import models


class Turn(models.Model):

    name = models.CharField('Name', max_length=50, null=False, blank=False)
    opening_time = models.TimeField()
    closing_time = models.TimeField()

    class Meta:
        managed = True
        db_table = 'reservations_turn'
        verbose_name = 'Turn'
        verbose_name_plural = 'Turns'

    def __str__(self):
        return f'{self.name}'
