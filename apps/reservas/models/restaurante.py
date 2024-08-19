from django.db import models


class Restaurantes(models.Model):
    nombre      = models.CharField('Nombre', max_length=30, null=False)
    descripcion = models.TextField('Descripcion', null = True)
    logo        = models.FilePathField('Logo', path = 'media/imgs')
    
    class Meta:
        managed             = True
        db_table            = 'reservas\".\"restaurante'
        verbose_name        = 'Restaurante'
        verbose_name_plural = 'Restaurantes'

    def __str__(self):
        return f'{self.nombre}'
    
