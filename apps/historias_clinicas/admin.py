from django.contrib import admin
from .models import HistoriaClinica

@admin.register(HistoriaClinica)
class HistoriaClinicaAdmin(admin.ModelAdmin):
    list_display = ('id', 'paciente', 'medico', 'fecha_consulta', 'diagnostico_corto', 'is_deleted')
    list_filter = ('is_deleted', 'fecha_consulta', 'medico')
    search_fields = ('paciente__nombre_completo', 'paciente__dni', 'diagnostico', 'motivo_consulta')

    def diagnostico_corto(self, obj):
        return obj.diagnostico[:50] + ("..." if len(obj.diagnostico) > 50 else "")
    diagnostico_corto.short_description = "Diagnóstico"

    def get_queryset(self, request):
        # En admin mostrar todas incluyendo eliminadas lógicamente para auditoría
        return HistoriaClinica.all_with_deleted.all()
