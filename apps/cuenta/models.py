import os
import requests
import json
import logging
from decouple import config
from requests.exceptions import RequestException

from django.db import models, IntegrityError
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from rest_framework_simplejwt.tokens import RefreshToken
import random

from apps.cuenta.validators             import *

class UserManager(BaseUserManager):

    def create_user(self, username, email, origen, cedula, nombre_apellido, password=None):
        if not username:
            raise ValueError('El usuario debe tener un nombre de usuario')
        if not email:
            raise ValueError('El usuario debe tener un correo electrónico')

        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            origen=origen,
            cedula=cedula,
            nombre_apellido=nombre_apellido,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, origen, cedula, nombre_apellido, password=None):
        user = self.create_user(
            username=username,
            email=email,
            origen=origen,
            cedula=cedula,
            nombre_apellido=nombre_apellido,
            password=password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    V = 'V'
    E = 'E'

    ORIGEN = (
        (V, 'V'),
        (E, 'E'),
    )

    verificacion = models.CharField('Verificacion', max_length=10, unique=True, blank=True, null=True)
    username = models.CharField('Usuario', max_length=20, unique=True)
    email = models.EmailField('Correo', max_length=255, unique=True)
    origen = models.CharField('Origen', max_length=1, choices=ORIGEN)
    cedula = models.IntegerField('Cédula', validators=[data_cedula])
    nombre_apellido = models.CharField('Nom/Ape', max_length=255, blank=True, null=True)
    pregunta_01 = models.CharField('Preg. 01', max_length=255, default='INDETERMINADA')
    pregunta_02 = models.CharField('Preg. 02', max_length=255, default='INDETERMINADA')
    pregunta_03 = models.CharField('Preg. 03', max_length=255, default='INDETERMINADA')
    respuesta_01 = models.CharField('Resp. 01', max_length=255, default='INDETERMINADA')
    respuesta_02 = models.CharField('Resp. 02', max_length=255, default='INDETERMINADA')
    respuesta_03 = models.CharField('Resp. 03', max_length=255, default='INDETERMINADA')
    fecha_registro = models.DateTimeField('Fecha Registro', auto_now_add=True)
    fecha_actualizacion = models.DateTimeField('Fecha Actualización', auto_now=True)
    is_verified = models.BooleanField('VERIFICADO', default=True)
    is_active = models.BooleanField('ACTIVO', default=True)
    is_staff = models.BooleanField('STAFF', default=False)
    is_superuser = models.BooleanField('ROOT', default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['origen', 'cedula', 'nombre_apellido', 'email']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            self.verificacion = ''.join(str(random.randint(0, 9)) for _ in range(10))
            
            resultado = data_cedula(self.cedula)
            self.nombre_apellido, self.origen = resultado

            print(self.origen)

            super().save(*args, **kwargs)
        except IntegrityError:
            self.save(*args, **kwargs)

    class Meta:
        managed             = True
        db_table            = 'cuenta\".\"usuario'
        verbose_name        = 'Usuario'
        verbose_name_plural = 'Usuarios'
        unique_together     = ('origen','cedula')

    USERNAME_FIELD  = 'username'
    REQUIRED_FIELDS = ['origen','cedula','nombre_apellido','email']

    def __str__(self):
        return self.username

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {'refresh': str(refresh), 'access': str(refresh.access_token)}