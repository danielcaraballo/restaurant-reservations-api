from django.contrib                           import admin
from django.urls                              import path, include, re_path
from rest_framework                           import routers
from drf_yasg.views                           import get_schema_view
from drf_yasg                                 import openapi
from apps.reportes.views.acta                 import generar_reporte_ingreso
from apps.reportes.views.acta_salida          import generar_reporte_salida
from rest_framework                           import permissions
from apps.auxiliares.views.subcategoria       import filtrar_subcategorias
from apps.gestion.views.salida                import filtrar_codigos_lote

from apps.frontend.views                      import inicio

router = routers.DefaultRouter()

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="API documentación del Sistema de gestion de almacén",
        terms_of_service="https://www.example.com/policies/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="sin licencia"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', inicio , name='inicio'),
    path('admin/', admin.site.urls),
    path('reporte/',                                 include('apps.reportes.urls')),
    path('reporte_ingreso/<int:ingreso_id>/', generar_reporte_ingreso, name='reporte_ingreso'),
    path('reporte_salida/<int:salida_id>/', generar_reporte_salida, name='reporte_salida'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('subcategoria/filtro/<int:categoria_id>/', filtrar_subcategorias, name='filtrar_subcategorias'),
    path('salidasbienes/filtro/<int:bien_id>/', filtrar_codigos_lote, name='filtrar_codigos_lote'),
    path('geo/',                include('apps.geo.urls.estados')),
    path('geo/',                include('apps.geo.urls.municipios')),
    path('geo/',                include('apps.geo.urls.parroquias')),
    path('cuenta/',             include('apps.cuenta.urls')),
]