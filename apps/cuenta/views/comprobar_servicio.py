from rest_framework                     import status
from rest_framework.response            import Response
from rest_framework.decorators          import api_view

from drf_yasg.utils                    import swagger_auto_schema


@swagger_auto_schema(   
                        methods                 = ['get'],
                        operation_description   = "Comprobar disponibilidad del servicio",
                        responses               =   {
                                                        status.HTTP_200_OK:             'Servicio disponible!'
                                                    },
                        tags                    = ['disponiblidad de servicio'],
                    )
@api_view(['get',])
def comprobar_servicio(request):
    return Response(status = status.HTTP_200_OK)
