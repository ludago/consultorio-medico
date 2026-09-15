from django.contrib import admin
from apps.core.utils import safe_get_perfil
from .models import LogAuditoria


@admin.register(LogAuditoria)
class LogAuditoriaAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'usuario', 'accion', 'entidad', 'entidad_id', 'ip_origen')
    list_filter = ('accion', 'entidad', 'timestamp')
    search_fields = ('usuario__username', 'entidad', 'detalles')
    readonly_fields = ('timestamp', 'usuario', 'accion', 'entidad', 'entidad_id', 'detalles', 'ip_origen')

    def has_module_permission(self, request, obj=None):
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        perfil = safe_get_perfil(request.user)
        return perfil and perfil.rol in ['ADMIN', 'DEV']

    def has_view_permission(self, request, obj=None):
        return self.has_module_permission(request, obj)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
