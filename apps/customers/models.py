from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
import re

# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="customer")
    phone = models.CharField('Phone', max_length=15, blank=True, null=True)

    # En caso de roles específicos para clientes, considera activar los siguientes campos
    # groups = models.ManyToManyField(
    #     'auth.Group',
    #     related_name='customer_set',
    #     blank=True
    # )

    # user_permissions = models.ManyToManyField(
    #     'auth.Permission',
    #     related_name='customer_set',
    #     blank=True
    # )

    # Valida que el número de teléfono tenga entre 10 y 15 dígitos, con un prefijo opcional '+'
    def clean(self):
        if self.phone and not re.match(r'^\+?\d{10,15}$', self.phone):
            raise ValidationError(
                'Phone number must be between 10 and 15 digits, optionally starting with a "+".')

    def __str__(self):
        return f'{self.user.username} - {self.user.first_name} {self.user.last_name}'
