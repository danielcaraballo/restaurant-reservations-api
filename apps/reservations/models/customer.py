from django.db import models


class Customer(models.Model):

    name = models.CharField('Name', max_length=50)
    last_name = models.CharField('Last Name', max_length=50)
    email = models.EmailField('Email', max_length=100)
    phone = models.CharField('Phone', max_length=20, blank=True)

    class Meta:
        managed = True
        db_table = 'reservations_customer'
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'

    def __str__(self):
        return f'{self.name} {self.last_name}'
