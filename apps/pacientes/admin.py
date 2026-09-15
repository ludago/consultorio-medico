from django.contrib import admin
from apps.core.utils import safe_get_perfil
from .models import ObraSocial, Paciente


@admin.register(ObraSocial)
class ObraSocialAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'codigo_nomenclador')
    search_fields = ('nombre',)

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


@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('nombre_completo', 'dni', 'telefono', 'obra_social', 'proxima_fecha_recall', 'consentimiento_datos', 'is_deleted')
    search_fields = ('nombre_completo', 'dni', 'telefono', 'email')
    list_filter = ('obra_social', 'consentimiento_datos', 'is_deleted')
    readonly_fields = ('fecha_registro', 'deleted_at')

    def get_queryset(self, request):
        qs = Paciente.all_with_deleted.get_queryset()
        if request.user.is_superuser:
            return qs
        perfil = safe_get_perfil(request.user)
        if perfil and perfil.rol == 'DEV':
            return qs
        return qs.filter(is_deleted=False)

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
