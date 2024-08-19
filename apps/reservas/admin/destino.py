from  django.contrib                      import admin
from  apps.auxiliares.models.destino      import Destino
from  django.utils.html 			      import format_html

class AdminDestino(admin.ModelAdmin):
    
    # Accesos directos del lado derecho
    def ver(self, obj):
        return format_html('<a class="btn btn-primary btn-sm" href="/admin/auxiliares/destino/{}/change/"><i class="nav-icon fas fa-eye" title="Ver detalles"></i></a>', obj.id)
    
    def eliminar(self, obj):
        return format_html('<a class="btn btn-danger btn-sm" href="/admin/auxiliares/destino/{}/delete/"><i class="nav-icon fas fa-trash"></i></a>', obj.id)

    def has_add_permission(self, request, obj=None):
        return True
    
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
    
    """def codigo_de_lote (self, obj):
        return format_html('<a class="btn btn-success btn-sm" title="codigo de lote">'+'<strong>'+str(obj.codigo+'</strong>'))"""
    
    list_display        = ('destino',)#'descripcion', 'ver','eliminar')
    list_filter         = ()
    search_fields       = []
    list_display_links  = None
    actions             = None


admin.site.register(Destino, AdminDestino)