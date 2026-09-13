from django.contrib import admin
from .models import LogAuditoria

@admin.register(LogAuditoria)
class LogAuditoriaAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'usuario', 'accion', 'entidad', 'entidad_id', 'ip_origen')
    list_filter = ('accion', 'entidad', 'timestamp')
    search_fields = ('usuario__username', 'entidad', 'detalles')
    readonly_fields = ('timestamp', 'usuario', 'accion', 'entidad', 'entidad_id', 'detalles', 'ip_origen')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
