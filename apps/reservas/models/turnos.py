from django.db import models

class Turnos(models.Model):
    
    nombre          = models.CharField('Nombre del turno', null=False, blank=False)
    descripcion     = models.CharField('Descripcion del turno', null= False, blank=False)
    hora_apertura   = models.TimeField() 
    hora_cierre     = models.TimeField()

    class Meta:
        managed             = True
        db_table            = 'reservas\".\"turnos'
        verbose_name        = 'Turno'
        verbose_name_plural = 'Turnos'

    def __str__(self):
        return f'{self.nombre}'