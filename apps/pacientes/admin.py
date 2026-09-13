from django.contrib import admin
from .models import ObraSocial, Paciente

@admin.register(ObraSocial)
class ObraSocialAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'codigo_nomenclador')
    search_fields = ('nombre',)

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('nombre_completo', 'dni', 'telefono', 'obra_social', 'proxima_fecha_recall', 'consentimiento_datos')
    search_fields = ('nombre_completo', 'dni', 'telefono', 'email')
    list_filter = ('obra_social', 'consentimiento_datos')
