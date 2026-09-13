from django.db import models
from django.contrib.auth.models import User

class LogAuditoria(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    accion = models.CharField(max_length=50, help_text="CREAR / EDITAR / ELIMINAR / VER / EXPORTAR")
    entidad = models.CharField(max_length=100, help_text="Ej: HistoriaClinica, Paciente, Turno")
    entidad_id = models.CharField(max_length=50, blank=True, null=True)
    detalles = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_origen = models.GenericIPAddressField(default="127.0.0.1")

    class Meta:
        verbose_name = "Registro de Auditoría"
        verbose_name_plural = "Registros de Auditoría"
        ordering = ['-timestamp']

    def __str__(self):
        usr = self.usuario.username if self.usuario else "Sistema/Anónimo"
        return f"[{self.timestamp.strftime('%d/%m/%Y %H:%M')}] {usr} -> {self.accion} {self.entidad} (ID: {self.entidad_id})"
