from django.contrib import admin
from apps.core.utils import safe_get_perfil
from .models import ConfiguracionSistema


@admin.register(ConfiguracionSistema)
class ConfiguracionSistemaAdmin(admin.ModelAdmin):
    list_display = ('nombre_consultorio', 'max_medicos_permitidos', 'modo_demo', 'telefono_whatsapp_empresa', 'fecha_actualizacion')

    def has_module_permission(self, request, obj=None):
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser and request.user.username in ['desarrollador', 'dev', 'admin_dev']:
            return True
        perfil = safe_get_perfil(request.user)
        return perfil and perfil.rol == 'DEV'

    def has_view_permission(self, request, obj=None):
        return self.has_module_permission(request, obj)

    def has_change_permission(self, request, obj=None):
        return self.has_module_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False
