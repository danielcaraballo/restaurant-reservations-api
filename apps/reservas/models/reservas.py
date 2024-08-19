from django.db import models

from .clientes import Clientes
from .areas import Areas
from .mesas import DisponibilidadMesas
from .turnos import Turnos

class Reservas(models.Model):

    num_invitados = models.IntegerField('N° de invitados', blank=True)
    estatus       = models.CharField('Estatus', max_length=50)
    cliente       = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    area          = models.ForeignKey(Areas, on_delete=models.CASCADE)
    fecha_reserva = models.ForeignKey(DisponibilidadMesas, related_name='fecha', on_delete=models.CASCADE)
    turno_reserva = models.ForeignKey(Turnos, on_delete=models.CASCADE)
    
   
    class Meta:
        managed             = True
        db_table            = 'reservas\".\"reservas'
        verbose_name        = 'Reserva'
        verbose_name_plural = 'Reservas'

    def __str__(self):
        return f'{self.cliente} {self.turno_reserva}'
    
