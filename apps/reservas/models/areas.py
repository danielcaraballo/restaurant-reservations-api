from django.db import models

class Areas (models.Model):

    descripcion = models.CharField('Descripción', max_length= 30, null = False)
    estatus     = models.BooleanField('Estatus', null = False)
   
    class Meta:
        managed             = True
        db_table            = 'reservas\".\"areas'
        verbose_name        = 'Área'
        verbose_name_plural = 'Áreas'

    def __str__(self):
        return f'{self.descripcion}'
    
