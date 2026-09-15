from django.contrib import admin
from .models import Turno, FacturaConsulta


@admin.register(Turno)
class TurnoAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha', 'hora', 'paciente', 'medico', 'estado', 'sede', 'consultorio')
    list_filter = ('estado', 'fecha', 'medico', 'sede')
    search_fields = ('paciente__nombre_completo', 'paciente__dni', 'medico__nombre_completo')
    date_hierarchy = 'fecha'

    def has_module_permission(self, request, obj=None):
        """Solo RECEPCION, ADMIN y DEV pueden ver Turnos en admin."""
        if not request.user.is_authenticated:
            return False
        perfil = getattr(request.user, 'perfil_usuario', None)
        if perfil and perfil.rol in ['RECEPCION', 'ADMIN', 'DEV']:
            return True
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        perfil = getattr(request.user, 'perfil_usuario', None)
        if perfil and perfil.rol in ['RECEPCION', 'ADMIN', 'DEV']:
            return True
        return request.user.is_superuser

    def has_add_permission(self, request):
        """Solo RECEPCION y ADMIN pueden crear turnos."""
        perfil = getattr(request.user, 'perfil_usuario', None)
        if perfil and perfil.rol in ['RECEPCION', 'ADMIN']:
            return True
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        perfil = getattr(request.user, 'perfil_usuario', None)
        if perfil and perfil.rol in ['RECEPCION', 'ADMIN', 'DEV']:
            return True
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        """Solo DEV puede eliminar turnos."""
        return request.user.is_superuser

    def get_queryset(self, request):
        """Filtrar turnos por medico si el usuario es medico."""
        qs = super().get_queryset(request)
        perfil = getattr(request.user, 'perfil_usuario', None)
        if perfil and perfil.rol == 'MEDICO' and hasattr(request.user, 'perfil_medico'):
            qs = qs.filter(medico=request.user.perfil_medico)
        return qs


@admin.register(FacturaConsulta)
class FacturaConsultaAdmin(admin.ModelAdmin):
    list_display = ('id', 'turno', 'monto', 'tipo_comprobante', 'cae', 'fecha_emision')

    def has_module_permission(self, request, obj=None):
        """Solo ADMIN y DEV pueden ver Facturas."""
        if not request.user.is_authenticated:
            return False
        perfil = getattr(request.user, 'perfil_usuario', None)
        if perfil and perfil.rol in ['ADMIN', 'DEV']:
            return True
        return request.user.is_superuser
