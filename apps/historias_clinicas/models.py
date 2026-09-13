from django.db import models
from django.utils import timezone
from apps.pacientes.models import Paciente
from apps.usuarios.models import Medico

class HistoriaClinicaQuerySet(models.QuerySet):
    def activas(self):
        return self.filter(is_deleted=False)

    def eliminadas(self):
        return self.filter(is_deleted=True)

class HistoriaClinicaManager(models.Manager):
    def get_queryset(self):
        return HistoriaClinicaQuerySet(self.model, using=self._db).filter(is_deleted=False)

    def eliminadas(self):
        return HistoriaClinicaQuerySet(self.model, using=self._db).filter(is_deleted=True)

    def todas_incluyendo_eliminadas(self):
        return HistoriaClinicaQuerySet(self.model, using=self._db)

class HistoriaClinica(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='historias_clinicas')
    medico = models.ForeignKey(Medico, on_delete=models.RESTRICT, related_name='historias_atendidas')
    fecha_consulta = models.DateTimeField(default=timezone.now)
    motivo_consulta = models.TextField(help_text="Motivo de la consulta reportado por el paciente")
    notas_evolucion = models.TextField(blank=True, help_text="Examen físico, observaciones y evolución")
    diagnostico = models.TextField(help_text="Diagnóstico o hipótesis diagnóstica")
    tratamiento_prescrito = models.TextField(blank=True, help_text="Indicaciones médicas y tratamiento")
    receta_electronica = models.TextField(blank=True, null=True, help_text="Texto / formato de receta electrónica (preparado)")
    
    # Soft-delete obligatorio Ley 26.529 (Retención 10 años)
    is_deleted = models.BooleanField(default=False, help_text="Marca de borrado lógico para auditoría y cumplimiento legal")
    deleted_at = models.DateTimeField(blank=True, null=True)

    objects = HistoriaClinicaManager()
    all_with_deleted = models.Manager()

    class Meta:
        verbose_name = "Historia Clínica"
        verbose_name_plural = "Historias Clínicas"
        ordering = ['-fecha_consulta']

    def __str__(self):
        return f"Consulta HC #{self.id} - {self.paciente.nombre_completo} ({self.fecha_consulta.strftime('%d/%m/%Y')})"

    def delete(self, using=None, keep_parents=False):
        """Soft delete según Ley 26.529"""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(using=using)
