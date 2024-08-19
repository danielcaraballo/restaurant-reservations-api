
from rest_framework                     import serializers
from apps.cuenta.models                 import User
from django.contrib                     import auth
from rest_framework.exceptions          import AuthenticationFailed


from apps.cuenta.models import User as Model
from rest_framework_simplejwt.serializers   import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token                       = super().get_token(user)
        #token['id']                 = user.id
        #token['origen']             = user.origen
        #token['cedula']             = user.cedula
        #token['email']              = user.email
        #token['verificacion']       = user.verificacion
        return token
    

class LoginSerializer(serializers.ModelSerializer):
    groups = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name',) 
    email = serializers.EmailField()

    def validate_email(self, value):
        lower_email = value.lower()
        if User.objects.filter(email__iexact=lower_email).exists():
            raise serializers.ValidationError("Duplicate")
        return lower_email

    class Meta:
        model   = Model
        fields  = (
                    'id',
                    'verificacion',
                    'username',
                    'email',
                    'origen',
                    'cedula',
                    'nombre_apellido',
                    'pregunta_01',
                    'pregunta_02',
                    'pregunta_03',
                    'respuesta_01',
                    'respuesta_02',
                    'respuesta_03',
                    #'password',
                    #'is_active',
                    'is_staff',
                    #'is_superuser',
                    'groups',
                    'user_permissions'
                    )