from django.contrib import admin
from .models import LogAuditoria


@admin.register(LogAuditoria)
class LogAuditoriaAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'usuario', 'accion', 'entidad', 'entidad_id', 'ip_origen')
    list_filter = ('accion', 'entidad', 'timestamp')
    search_fields = ('usuario__username', 'entidad', 'detalles')
    readonly_fields = ('timestamp', 'usuario', 'accion', 'entidad', 'entidad_id', 'detalles', 'ip_origen')

    def has_module_permission(self, request, obj=None):
        """Solo ADMIN y DEV pueden ver Auditoria."""
        if not request.user.is_authenticated:
            return False
        perfil = getattr(request.user, 'perfil_usuario', None)
        if perfil and perfil.rol in ['ADMIN', 'DEV']:
            return True
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        perfil = getattr(request.user, 'perfil_usuario', None)
        if perfil and perfil.rol in ['ADMIN', 'DEV']:
            return True
        return request.user.is_superuser

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
