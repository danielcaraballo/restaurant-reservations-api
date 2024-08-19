
from rest_framework                     import serializers


class SoliciarReinicioClaveSerializer(serializers.Serializer):
    email           = serializers.EmailField()
    redirect_url    = serializers.CharField(max_length=500, required = False)

    class Meta:
        fields = ['email']


