from  django.contrib                      import admin
from  apps.gestion.models.lote            import Lote
from  django.utils.html 			      import format_html

class AdminLote(admin.ModelAdmin):


     # Accesos directos del lado derecho
    def ver(self, obj):
        return format_html('<a class="btn btn-primary btn-sm" href="/admin/gestion/lote/{}/change/"><i class="nav-icon fas fa-eye" title="Ver detalles"></i></a>', obj.id)
    
    def eliminar(self, obj):
        return format_html('<a class="btn btn-danger btn-sm" href="/admin/gestion/lote/{}/delete/"><i class="nav-icon fas fa-trash"></i></a>', obj.id)

    def has_add_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
    
    def Cantidad(self, obj):
        return format_html('<a class="btn btn-success btn-sm" title="cantidad">'+str(obj.cantidad)+'   <i class="nav-icon fas fa-box"></i></a>'+'</a>')
   
    list_display        = ('codigo_de_lote','bien','Cantidad','ver',)
    list_filter         = []
    search_fields       = []
    list_display_links  = None
    actions             = None


admin.site.register(Lote, AdminLote)
