from  django.contrib                      import admin

#from django.contrib.auth import has_view_permission

from  apps.gestion.models.ingreso         import Ingreso, IngresosBienes
from  django.utils.html 			      import format_html
from  apps.gestion.forms                  import IngresoForm
from django.urls                          import reverse
from django.utils.safestring              import mark_safe
from django.http                          import HttpResponse
from django.http                          import HttpResponseRedirect
from simple_history.admin                 import SimpleHistoryAdmin

class AdminIngresosBienesInline(admin.TabularInline):
    model = IngresosBienes
    extra = 0


class AdminIngreso(SimpleHistoryAdmin):
    
    inlines = [AdminIngresosBienesInline,]
     # Accesos directos del lado derecho
    def ver(self, obj):
        return format_html('<a class="btn btn-primary btn-sm" href="/admin/gestion/ingreso/{}/change/"><i class="nav-icon fas fa-eye" title="Ver detalles"></i></a>', obj.id)
    
    def eliminar(self, obj):
        return format_html('<a class="btn btn-danger btn-sm" href="/admin/gestion/ingreso/{}/delete/"><i class="nav-icon fas fa-trash"></i></a>', obj.id)

    def has_add_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        if request.user.groups.filter(name='Analista').exists():
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        if request.user.groups.filter(name='Analista').exists():
            return False
        return True
    
    
    def generar_reporte(self, obj):
        url = reverse("reporte_ingreso", args=[obj.id])
        return mark_safe(f'<a class="btn btn-secondary btn-sm" href="{url}"><i class="fas fa-file-alt" title="Generar reporte"></i></a>')
    
    def get_list_display(self, request):
        
        if request.user.is_superuser:
            #if request.user.is_superuser or request.user.is_staff:
            return ['proveedor','motivo','numero_factura','fecha_de_ingreso','hora_de_ingreso','codigo','observacion','ver','eliminar','generar_reporte',]

        for numero in request.user.groups.all():
            if str(numero) == 'Administrador':
            #if request.user.is_superuser or request.user.is_staff:
                return ['proveedor','motivo','numero_factura','fecha_de_ingreso','hora_de_ingreso','codigo','observacion','ver','eliminar','generar_reporte',]
            else:
                return ['proveedor','motivo','numero_factura','fecha_de_ingreso','hora_de_ingreso','codigo','observacion','generar_reporte',]  

    generar_reporte.short_description = "Acta"

  
    #list_display        = ('proveedor','motivo','numero_factura','fecha_de_ingreso','hora_de_ingreso','codigo','observacion','ver','eliminar','generar_reporte',)
    list_filter         = ('motivo',)
    search_fields       = []
    list_display_links  = None
    actions             = None

    exclude = ('municipio', 'parroquia')

    def fecha_de_ingreso(self, obj):
        return obj.fecha.strftime("%d/%m/%Y")
    
    def hora_de_ingreso(self, obj):
        return obj.hora.strftime('%I:%M %p')

    form = IngresoForm

    class Media:
            js  =   (
                        'js/combo_dependiente.js',
                    )  

admin.site.register(Ingreso, AdminIngreso)