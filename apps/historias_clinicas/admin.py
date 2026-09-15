from django.contrib import admin
from apps.core.utils import safe_get_perfil
from .models import HistoriaClinica


@admin.register(HistoriaClinica)
class HistoriaClinicaAdmin(admin.ModelAdmin):
    list_display = ('id', 'paciente', 'medico', 'fecha_consulta', 'diagnostico_corto', 'is_deleted')
    list_filter = ('is_deleted', 'fecha_consulta', 'medico')
    search_fields = ('paciente__nombre_completo', 'paciente__dni', 'diagnostico', 'motivo_consulta')
    readonly_fields = ('paciente', 'medico', 'fecha_consulta', 'motivo_consulta', 'diagnostico', 'notas_evolucion', 'tratamiento_prescrito', 'deleted_at')

    def diagnostico_corto(self, obj):
        diagnostico = obj.diagnostico or ''
        return diagnostico[:50] + ('...' if len(diagnostico) > 50 else '')
    diagnostico_corto.short_description = 'Diagnostico'

    def get_queryset(self, request):
        qs = HistoriaClinica.all_with_deleted.all()
        if request.user.is_superuser:
            return qs
        perfil = safe_get_perfil(request.user)
        if perfil and perfil.rol == 'DEV':
            return qs
        if perfil and perfil.rol == 'MEDICO' and hasattr(request.user, 'perfil_medico'):
            return qs.filter(medico=request.user.perfil_medico, is_deleted=False)
        return qs.filter(is_deleted=False)

    def has_module_permission(self, request, obj=None):
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        perfil = safe_get_perfil(request.user)
        return perfil and perfil.rol in ['MEDICO', 'ADMIN', 'DEV']

    def has_view_permission(self, request, obj=None):
        return self.has_module_permission(request, obj)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return self.has_module_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
