from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Customer(AbstractUser):
    phone = models.CharField('Phone', max_length=15, blank=True, null=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customer_set',
        blank=True
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customer_set',
        blank=True
    )

    def __str__(self):
        return f'{self.username} - {self.first_name} {self.last_name}'
