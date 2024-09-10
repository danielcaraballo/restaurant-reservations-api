from django.shortcuts                   import render

from rest_framework                     import status
from rest_framework.response            import Response

from apps.user.models                         import User as Model
from apps.nomina.models.trabajador              import Trabajador as TrabajadorModel

from apps.user.serializers.verificar_credencial   import Serializer as CredencialSerializers
from apps.nomina.serializers.datos_trabajador       import Serializer as TrabajadorSerializers


from rest_framework.decorators                  import api_view
from drf_yasg.utils                             import swagger_auto_schema

@swagger_auto_schema(   
                        methods                 = ['post'],
                        operation_description   = "Verificar credencial mediante código",
                        responses               =   {
                                                        status.HTTP_200_OK:             'Datos encontrados!',
                                                        status.HTTP_400_BAD_REQUEST:    'Error en la operación!'
                                                    },
                        tags                    = ['Verificar Credencial'],
                        request_body            = CredencialSerializers
                    )
@api_view(['POST'])
def verificar_credencial(request):
    verificacion    = request.data.get('verificacion', '')
    model = Model.objects.filter(verificacion = verificacion).values('origen','cedula').first()
    
    if model:
        origen = model["origen"]
        cedula = model["cedula"]

        trabajador_model = TrabajadorModel.objects.filter(origen =  origen, cedula = cedula).first()
        if trabajador_model:
            trabajador_serializer = TrabajadorSerializers(trabajador_model)

            return Response(trabajador_serializer.data, status = status.HTTP_200_OK)
    return Response({'message':'Código invalido!'}, status = status.HTTP_400_BAD_REQUEST)




def verificar_credencialB(request, verificacion = None):
    model = Model.objects.filter(verificacion = verificacion).values('origen','cedula').first()
    
    if model:
        origen_nomina = model["origen"]
        cedula_nomina = model["cedula"]

        model_nomina = TrabajadorModel.objects.filter(origen = origen_nomina, cedula = cedula_nomina,).values('origen','cedula','nombres_apellidos','clasificacion','cargo','dependencia','funcion','otra_funcion','entidad','numero_cuenta','anhio','estatus').first()

        if model_nomina:
            context ={} 
            context["data"] = model_nomina 
         
            return render(request, 'frontend/verificar_credencial.html', context)

    return render(request, 'frontend/documentacion.html',)