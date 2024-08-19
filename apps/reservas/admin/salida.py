from  django.contrib                      import admin, messages
from  apps.gestion.models.salida          import Salida, SalidasBienes
from  django.utils.html 			      import format_html
from  apps.gestion.forms                  import SalidasBienesForm
from  apps.auxiliares.models.responsable  import Responsable
from django.urls                          import reverse
from django.utils.safestring              import mark_safe
from django.http                          import HttpResponse
from django.http                          import HttpResponseRedirect
from apps.gestion.forms                   import SalidaForm



class AdminSalidasBienesInline(admin.TabularInline):
    model = SalidasBienes
    extra = 0
    #form = SalidasBienesForm
    class Media:
        js = ('js/select_codigo_lote.js',)

class AdminSalida(admin.ModelAdmin):
    
    inlines = [AdminSalidasBienesInline,]
     # Accesos directos del lado derecho
    def ver(self, obj):
        return format_html('<a class="btn btn-primary btn-sm" href="/admin/gestion/salida/{}/change/"><i class="nav-icon fas fa-eye" title="Ver detalles"></i></a>', obj.id)
    
    def eliminar(self, obj):
        return format_html('<a class="btn btn-danger btn-sm" href="/admin/gestion/salida/{}/delete/"><i class="nav-icon fas fa-trash"></i></a>', obj.id)

    def has_add_permission(self, request, obj=None):
        return True
    
    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        if request.user.groups.filter(name='Analista').exists():
            return False
        return True
    
    def get_list_display(self, request):
    
        if request.user.is_superuser:
            #if request.user.is_superuser or request.user.is_staff:
            return ['destino','motivo','jefe_de_almacen','destinatario','supervisor_de_seguridad','hora_de_salida','fecha_de_salida','ver','generar_reporte']

        for numero in request.user.groups.all():
            if str(numero) == 'Administrador':
            #if request.user.is_superuser or request.user.is_staff:
                return ['destino','motivo','jefe_de_almacen','destinatario','supervisor_de_seguridad','hora_de_salida','fecha_de_salida','ver','generar_reporte']
            else:
                return ['destino','motivo','jefe_de_almacen','destinatario','supervisor_de_seguridad','hora_de_salida','fecha_de_salida','generar_reporte']  

    def generar_reporte(self, obj):
        url = reverse("reporte_salida", args=[
            obj.id])
        return mark_safe(f'<a class="btn btn-secondary btn-sm" href="{url}"><i class="fas fa-file-alt" title="Generar reporte"></i></a>')

    generar_reporte.short_description = "Acta"
    
    #list_display        = ('destino','motivo','jefe_de_almacen','destinatario','supervisor_de_seguridad','hora_de_salida','fecha_de_salida','ver','generar_reporte')
    list_filter         = ('motivo',)
    search_fields       = []
    list_display_links  = None
    actions             = None

    exclude = ('municipio', 'parroquia')

    def fecha_de_salida(self, obj):
        return obj.fecha.strftime("%d/%m/%Y")
    
    def hora_de_salida(self, obj):
        return obj.hora.strftime('%I:%M %p')

    form = SalidaForm
    
    class Media:
            js  =   (
                        'js/combo_dependiente.js',
                    ) 

admin.site.register(Salida, AdminSalida)