from django.contrib import admin
from .models import Turno, FacturaConsulta

@admin.register(Turno)
class TurnoAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha', 'hora', 'paciente', 'medico', 'estado', 'sede', 'consultorio')
    list_filter = ('estado', 'fecha', 'medico', 'sede')
    search_fields = ('paciente__nombre_completo', 'paciente__dni', 'medico__nombre_completo')
    date_hierarchy = 'fecha'

@admin.register(FacturaConsulta)
class FacturaConsultaAdmin(admin.ModelAdmin):
    list_display = ('id', 'turno', 'monto', 'tipo_comprobante', 'cae', 'fecha_emision')
