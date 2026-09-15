from django.contrib import admin
from apps.core.utils import safe_get_perfil
from .models import Turno, FacturaConsulta


@admin.register(Turno)
class TurnoAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha', 'hora', 'paciente', 'medico', 'estado', 'sede', 'consultorio', 'is_deleted')
    list_filter = ('estado', 'fecha', 'medico', 'sede', 'is_deleted')
    search_fields = ('paciente__nombre_completo', 'paciente__dni', 'medico__nombre_completo')
    date_hierarchy = 'fecha'
    readonly_fields = ('fecha_creacion', 'deleted_at')

    def get_queryset(self, request):
        qs = Turno.all_with_deleted.get_queryset()
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
        return perfil and perfil.rol in ['RECEPCION', 'ADMIN', 'DEV']

    def has_view_permission(self, request, obj=None):
        return self.has_module_permission(request, obj)

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        perfil = safe_get_perfil(request.user)
        return perfil and perfil.rol in ['RECEPCION', 'ADMIN']

    def has_change_permission(self, request, obj=None):
        return self.has_module_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


@admin.register(FacturaConsulta)
class FacturaConsultaAdmin(admin.ModelAdmin):
    list_display = ('id', 'turno', 'monto', 'tipo_comprobante', 'cae', 'fecha_emision')

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
        return self.has_module_permission(request)

    def has_change_permission(self, request, obj=None):
        return self.has_module_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
