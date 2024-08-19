from django.db import models

from .clientes import Clientes

class Valoraciones(models.Model):

    comentario   = models.TextField('Comentario', blank=True)
    calificacion = models.IntegerField('Calificación', blank=True)
    cliente      = models.ForeignKey(Clientes, related_name='clientes', on_delete= models.SET_NULL)
   
    class Meta:
        managed             = True
        db_table            = 'reservas\".\"valoraciones'
        verbose_name        = 'Valoración'
        verbose_name_plural = 'Valoraciones'

    def __str__(self):
        return f'{self.comentario}'
    
