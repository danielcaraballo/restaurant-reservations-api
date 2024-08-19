from  django.contrib                      import admin
from  apps.gestion.models.almacen         import Almacen
from  apps.gestion.models.lote            import Lote
from  django.utils.html 			      import format_html
from  django.urls                         import reverse

class AdminAlmacen(admin.ModelAdmin):
    
    # Accesos directos del lado derecho
    def editar(self, obj):
        return format_html('<a class="btn btn-primary btn-sm" href="/admin/gestion/almacen/{}/change/"><i class="nav-icon fas fa-eye" title="Ver detalles"></i></a>', obj.id)
    
    def eliminar(self, obj):
        return format_html('<a class="btn btn-danger btn-sm" href="/admin/gestion/almacen/{}/delete/"><i class="nav-icon fas fa-trash"></i></a>', obj.id)

    def has_add_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return False
    
    def Cantidad(self, obj):
        return format_html('<a class="btn btn-success btn-sm" title="cantidad">'+str(obj.cantidad)+'  <i class="nav-icon fas fa-box"></i></a>'+'</a>')
   

    def fecha_de_ingreso(self, obj):
        return obj.fecha.strftime("%d/%m/%Y")
    
    def hora_de_ingreso(self, obj):
        return obj.hora.strftime('%I:%M %p')
    
    def ver(self, obj):
        lote_ids = Lote.objects.filter(bien=obj.bien).values_list('id', flat=True)
        if lote_ids:
            lote_ids_str = ','.join(map(str, lote_ids))
            url = reverse('admin:gestion_lote_changelist') + f'?id__in={lote_ids_str}'
            return format_html('<a class="btn btn-primary btn-sm" href="{}"><i class="fas fa-eye" title="Ver lotes"></i> {}</a>', url, '')
        else: 
            return '-'
    ver.short_description = 'Ver'

 
    list_display        = ('bien','Cantidad','ver')
    list_filter         = ()
    search_fields       = []
    list_display_links  = None
    actions             = None

admin.site.register(Almacen, AdminAlmacen)
