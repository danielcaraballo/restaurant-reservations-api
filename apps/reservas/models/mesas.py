from django.db import models

from apps.reservas.models.areas import Areas
from apps.reservas.models.turnos import Turnos


class Mesas(models.Model):
    
    num_mesa    = models.IntegerField('Número de mesa', null = False)
    capacidad   = models.IntegerField('Capacidad', null = False)
    area        = models.ForeignKey(Areas, related_name='Area', on_delete= models.PROTECT)
    estatus     = models.BooleanField('Estatus', null = False)
    
    class Meta:
        managed             = True
        db_table            = 'reservas\".\"mesas'
        verbose_name        = 'Mesa'
        verbose_name_plural = 'Mesas'

    def __str__(self):
        return f'{self.num_mesa}'
    


class DisponibilidadMesas(models.Model):
    
    mesa    = models.ForeignKey(Mesas, on_delete=models.CASCADE)
    fecha   = models.TimeField()
    estatus = models.BooleanField('Estatus', default=True)
    turno   = models.ForeignKey(Turnos, on_delete=models.CASCADE)

    class Meta:
        managed             = True
        db_table            = 'reservas\".\"disponibilidad_mesas'
        verbose_name        = 'Disponibilidad'
        verbose_name_plural = 'Disponibilidades'


    def __str__(self):
        return f'{self.mesa}'

    
    


    
