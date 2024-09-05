
from rest_framework                     import serializers
from rest_framework_simplejwt.tokens    import RefreshToken, TokenError


class SalirSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {'bad_token': ('El token ha expirado o es invalido')}

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail('error_messages')
