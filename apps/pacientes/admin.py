from django.contrib import admin
from .models import ObraSocial, Paciente


@admin.register(ObraSocial)
class ObraSocialAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'codigo_nomenclador')
    search_fields = ('nombre',)

    def has_module_permission(self, request, obj=None):
        """Solo ADMIN y DEV pueden ver Obras Sociales."""
        if not request.user.is_authenticated:
            return False
        perfil = getattr(request.user, 'perfil_usuario', None)
        if perfil and perfil.rol in ['ADMIN', 'DEV']:
            return True
        return request.user.is_superuser


@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('nombre_completo', 'dni', 'telefono', 'obra_social', 'proxima_fecha_recall', 'consentimiento_datos')
    search_fields = ('nombre_completo', 'dni', 'telefono', 'email')
    list_filter = ('obra_social', 'consentimiento_datos')

    def has_module_permission(self, request, obj=None):
        """Solo ADMIN y DEV pueden gestionar Pacientes."""
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
        perfil = getattr(request.user, 'perfil_usuario', None)
        if perfil and perfil.rol in ['ADMIN', 'DEV']:
            return True
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        perfil = getattr(request.user, 'perfil_usuario', None)
        if perfil and perfil.rol in ['ADMIN', 'DEV']:
            return True
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        """Solo DEV puede eliminar pacientes."""
        return request.user.is_superuser
