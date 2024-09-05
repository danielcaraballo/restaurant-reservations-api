import random
import logging
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from rest_framework_simplejwt.tokens import RefreshToken
from apps.user.validators import data_cedula

logger = logging.getLogger(__name__)

class UserManager(BaseUserManager):
    def create_user(self, username, email, name, last_name, password=None):
        if not username or not email:
            raise ValueError('The user must have a username and an email address')

        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            name=name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, name, last_name, password=None):
        user = self.create_user(
            username=username,
            email=email,
            name=name,
            last_name=last_name,
            password=password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    verification = models.CharField('Verification', max_length=10, unique=True, blank=True, null=True)
    username = models.CharField('Username', max_length=20, unique=True)
    email = models.EmailField('Email', max_length=255, unique=True)
    name = models.CharField('Name', max_length=255, blank=True, null=True)
    last_name = models.CharField('Last Name', max_length=255, blank=True, null=True)
    
    fecha_registro = models.DateTimeField('Registration Date', auto_now_add=True)
    fecha_actualizacion = models.DateTimeField('Update Date', auto_now=True)
    
    is_verified = models.BooleanField('Verified', default=True)
    is_active = models.BooleanField('Active', default=True)
    is_staff = models.BooleanField('Staff', default=False)
    is_superuser = models.BooleanField('Superuser', default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'last_name', 'email']

    def save(self, *args, **kwargs):
        if not self.pk:  # Check if the instance is being created
            self.verification = ''.join(str(random.randint(0, 9)) for _ in range(10))
            # Removed the unnecessary code related to `data_cedula` and assignments
        super().save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = 'users_user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {'refresh': str(refresh), 'access': str(refresh.access_token)}
