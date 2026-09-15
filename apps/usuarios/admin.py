from django.contrib import admin
from .models import Sede, Consultorio, Especialidad, Medico, MedicoSede, PerfilUsuario


@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('user', 'rol', 'activo')
    list_filter = ('rol', 'activo')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')


@admin.register(Sede)
class SedeAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'direccion', 'telefono', 'activa')

@admin.register(Consultorio)
class ConsultorioAdmin(admin.ModelAdmin):
    list_display = ('nombre_numero', 'sede')

@admin.register(Especialidad)
class EspecialidadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')

class MedicoSedeInline(admin.TabularInline):
    model = MedicoSede
    extra = 1

@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_display = ('nombre_completo', 'matricula_profesional', 'telefono_whatsapp', 'activo')
    list_filter = ('activo', 'especialidades')
    search_fields = ('nombre_completo', 'matricula_profesional', 'user__username')
    inlines = [MedicoSedeInline]
