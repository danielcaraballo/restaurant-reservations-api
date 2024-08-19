from django.db import models

class Clientes(models.Model):

    nombre   = models.CharField('Nombre', max_length=50)
    apellido = models.CharField('Apellido', max_length=50)
    correo   = models.CharField('Correo', max_length=100)
    telefono = models.IntegerField('Telefono', blank=True)
   
    class Meta:
        managed             = True
        db_table            = 'reservas\".\"clientes'
        verbose_name        = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return f'{self.nombre} {self.apellido}'
    
