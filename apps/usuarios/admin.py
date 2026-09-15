from django.contrib import admin
from apps.core.utils import safe_get_perfil
from .models import Sede, Consultorio, Especialidad, Medico, MedicoSede, PerfilUsuario


def _user_can_admin(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return True
    perfil = safe_get_perfil(request.user)
    return perfil and perfil.rol in ['ADMIN', 'DEV']


@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('user', 'rol', 'activo')
    list_filter = ('rol', 'activo')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')

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


@admin.register(Sede)
class SedeAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'direccion', 'telefono', 'activa')

    def has_module_permission(self, request, obj=None):
        return _user_can_admin(request)

    def has_view_permission(self, request, obj=None):
        return _user_can_admin(request)

    def has_add_permission(self, request):
        return _user_can_admin(request)

    def has_change_permission(self, request, obj=None):
        return _user_can_admin(request)

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


@admin.register(Consultorio)
class ConsultorioAdmin(admin.ModelAdmin):
    list_display = ('nombre_numero', 'sede')

    def has_module_permission(self, request, obj=None):
        return _user_can_admin(request)

    def has_view_permission(self, request, obj=None):
        return _user_can_admin(request)

    def has_add_permission(self, request):
        return _user_can_admin(request)

    def has_change_permission(self, request, obj=None):
        return _user_can_admin(request)

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


@admin.register(Especialidad)
class EspecialidadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')

    def has_module_permission(self, request, obj=None):
        return _user_can_admin(request)

    def has_view_permission(self, request, obj=None):
        return _user_can_admin(request)

    def has_add_permission(self, request):
        return _user_can_admin(request)

    def has_change_permission(self, request, obj=None):
        return _user_can_admin(request)

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


class MedicoSedeInline(admin.TabularInline):
    model = MedicoSede
    extra = 1


@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_display = ('nombre_completo', 'matricula_profesional', 'telefono_whatsapp', 'activo')
    list_filter = ('activo', 'especialidades')
    search_fields = ('nombre_completo', 'matricula_profesional', 'user__username')
    inlines = [MedicoSedeInline]

    def has_module_permission(self, request, obj=None):
        return _user_can_admin(request)

    def has_view_permission(self, request, obj=None):
        return _user_can_admin(request)

    def has_add_permission(self, request):
        return _user_can_admin(request)

    def has_change_permission(self, request, obj=None):
        return _user_can_admin(request)

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
