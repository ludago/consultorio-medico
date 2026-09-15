from django.contrib import admin
from .models import HistoriaClinica


@admin.register(HistoriaClinica)
class HistoriaClinicaAdmin(admin.ModelAdmin):
    list_display = ('id', 'paciente', 'medico', 'fecha_consulta', 'diagnostico_corto', 'is_deleted')
    list_filter = ('is_deleted', 'fecha_consulta', 'medico')
    search_fields = ('paciente__nombre_completo', 'paciente__dni', 'diagnostico', 'motivo_consulta')
    readonly_fields = ('paciente', 'medico', 'fecha_consulta', 'motivo_consulta', 'diagnostico', 'notas_evolucion', 'tratamiento_prescrito', 'deleted_at')

    def diagnostico_corto(self, obj):
        return obj.diagnostico[:50] + ("..." if len(obj.diagnostico) > 50 else "")
    diagnostico_corto.short_description = "Diagnóstico"

    def get_queryset(self, request):
        """Filtrar HC por medico si el usuario es medico, y excluir eliminadas."""
        qs = HistoriaClinica.all_with_deleted.all()
        perfil = getattr(request.user, 'perfil_usuario', None)
        
        # Dev ve todo
        if request.user.is_superuser or (perfil and perfil.rol == 'DEV'):
            return qs
        
        # Medico solo ve sus HC activas
        if perfil and perfil.rol == 'MEDICO' and hasattr(request.user, 'perfil_medico'):
            return qs.filter(medico=request.user.perfil_medico, is_deleted=False)
        
        # Admin ve todas las activas
        return qs.filter(is_deleted=False)

    def has_module_permission(self, request, obj=None):
        """Solo MEDICO, ADMIN y DEV pueden ver Historias Clinicas."""
        if not request.user.is_authenticated:
            return False
        perfil = getattr(request.user, 'perfil_usuario', None)
        if perfil and perfil.rol in ['MEDICO', 'ADMIN', 'DEV']:
            return True
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        perfil = getattr(request.user, 'perfil_usuario', None)
        if perfil and perfil.rol in ['MEDICO', 'ADMIN', 'DEV']:
            return True
        return request.user.is_superuser

    def has_add_permission(self, request):
        """Solo Medicos pueden crear HC (desde la vista, no desde admin)."""
        return False

    def has_change_permission(self, request, obj=None):
        """Solo Medicos pueden editar HC."""
        perfil = getattr(request.user, 'perfil_usuario', None)
        if perfil and perfil.rol in ['MEDICO', 'ADMIN', 'DEV']:
            return True
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        """Solo DEV puede eliminar HC (soft delete)."""
        return request.user.is_superuser
