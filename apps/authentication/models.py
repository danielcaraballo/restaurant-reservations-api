from django.db import models
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()


class AuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        """Permite autenticación con username o email"""
        user = None
        try:
            if '@' in username:  # Si contiene '@', asumimos que es un email
                user = User.objects.get(email=username)
            else:
                user = User.objects.get(username=username)

            if user and user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
