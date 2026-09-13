from django.contrib import admin
from .models import ConfiguracionSistema

@admin.register(ConfiguracionSistema)
class ConfiguracionSistemaAdmin(admin.ModelAdmin):
    list_display = ('nombre_consultorio', 'max_medicos_permitidos', 'modo_demo', 'telefono_whatsapp_empresa', 'fecha_actualizacion')

    def has_module_permission(self, request):
        """
        Restringe la visibilidad del módulo de Licencia/Configuración Global 
        únicamente al usuario Desarrollador del sistema (username 'desarrollador' o 'dev').
        """
        return request.user.is_superuser and request.user.username in ['desarrollador', 'dev', 'admin_dev']

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser and request.user.username in ['desarrollador', 'dev', 'admin_dev']

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser and request.user.username in ['desarrollador', 'dev', 'admin_dev']

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False
