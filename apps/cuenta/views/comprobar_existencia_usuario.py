from rest_framework                     import status
from rest_framework.response            import Response
from rest_framework.decorators          import api_view

from drf_yasg.utils                     import swagger_auto_schema

from apps.cuenta.models                 import User         as Model
from apps.nomina.models.trabajador      import Trabajador   as TrabajadorModel

from apps.cuenta.serializers.comprobar_existencia_usuario   import ComprobarExistenciaUsuarioSerializer
from apps.nomina.serializers.comprobar_datos                import ComprobarDatosSerializer

@swagger_auto_schema(   
                        methods                 = ['post'],
                        operation_description   = "Comprobar la existencia de un usuario",
                        responses               =   {
                                                        status.HTTP_200_OK:             'Existe el usuario!',
                                                        status.HTTP_400_BAD_REQUEST:    'No existe el usuario!'
                                                    },
                        tags                    = ['Creación de cuenta'],
                        request_body            = ComprobarExistenciaUsuarioSerializer
                    )
@api_view(['POST'])
def comprobar_existencia_usuario(request,):
    origen              = request.data.get('origen', '')
    cedula              = request.data.get('cedula', '')
    cuenta_bancaria     = request.data.get('cuenta_bancaria', '')

    trabajador_model = TrabajadorModel.objects.filter(origen = origen, cedula = cedula, cuenta_bancaria__endswith = cuenta_bancaria).first()
    
    if trabajador_model:
            model = Model.objects.filter(origen = origen, cedula = cedula).first()
            if model:
                return Response({'message':'Esta persona tiene cuenta de usuario'}, status = status.HTTP_400_BAD_REQUEST)
            else:
                serializer = ComprobarDatosSerializer(trabajador_model)
                return Response(serializer.data,  status = status.HTTP_200_OK)
    
    return Response({'message':'Datos errones o esta persona no es personal del MPPE'}, status = status.HTTP_404_NOT_FOUND)