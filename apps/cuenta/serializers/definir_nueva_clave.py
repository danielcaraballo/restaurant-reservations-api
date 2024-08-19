
from rest_framework                     import serializers
from apps.cuenta.models                 import User
from rest_framework.exceptions          import AuthenticationFailed
from django.contrib.auth.tokens         import PasswordResetTokenGenerator
from django.utils.encoding              import force_str
from django.utils.http                  import urlsafe_base64_decode


class SetNewPasswordSerializer(serializers.Serializer):
    password    = serializers.CharField(write_only = True)
    token       = serializers.CharField(write_only = True)
    uidb64      = serializers.CharField(write_only = True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password    = attrs.get('password')
            token       = attrs.get('token')
            uidb64      = attrs.get('uidb64')

            id          = force_str(urlsafe_base64_decode(uidb64))
            user        = User.objects.get(id = id)
            
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('El link es invalido', 401)

            user.set_password(password)
            user.save()

            return (user)
        except Exception as e:
            raise AuthenticationFailed('El link de reinicio es invalido', 401)
        return super().validate(attrs)