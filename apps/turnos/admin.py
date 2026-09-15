from django.contrib import admin
from .models import Turno, FacturaConsulta


@admin.register(Turno)
class TurnoAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha', 'hora', 'paciente', 'medico', 'estado', 'sede', 'consultorio', 'is_deleted')
    list_filter = ('estado', 'fecha', 'medico', 'sede', 'is_deleted')
    search_fields = ('paciente__nombre_completo', 'paciente__dni', 'medico__nombre_completo')
    date_hierarchy = 'fecha'
    readonly_fields = ('fecha_creacion', 'deleted_at')

    def get_queryset(self, request):
        """Mostrar solo turnos activos por defecto."""
        qs = Turno.all_with_deleted.get_queryset()
        if request.user.is_superuser or (getattr(request.user, 'perfil_usuario', None) and request.user.perfil_usuario.rol == 'DEV'):
            return qs
        perfil = getattr(request.user, 'perfil_usuario', None)
        if perfil and perfil.rol == 'MEDICO' and hasattr(request.user, 'perfil_medico'):
            return qs.filter(medico=request.user.perfil_medico, is_deleted=False)
        return qs.filter(is_deleted=False)

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
