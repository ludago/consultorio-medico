import hashlib
import json
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
    
    # Hash de integridad para verificar que el registro no fue alterado
    hash_integridad = models.CharField(max_length=64, blank=True, help_text="SHA-256 para verificar integridad del registro")

    class Meta:
        verbose_name = "Registro de Auditoría"
        verbose_name_plural = "Registros de Auditoría"
        ordering = ['-timestamp']

    def __str__(self):
        usr = self.usuario.username if self.usuario else "Sistema/Anónimo"
        return f"[{self.timestamp.strftime('%d/%m/%Y %H:%M')}] {usr} -> {self.accion} {self.entidad} (ID: {self.entidad_id})"

    def generar_hash(self):
        """Genera hash SHA-256 para verificar integridad del registro."""
        datos = {
            'usuario': self.usuario_id,
            'accion': self.accion,
            'entidad': self.entidad,
            'entidad_id': self.entidad_id,
            'detalles': self.detalles,
            'ip_origen': self.ip_origen,
        }
        # Ordenar para consistencia
        datos_ordenados = json.dumps(datos, sort_keys=True, default=str)
        return hashlib.sha256(datos_ordenados.encode()).hexdigest()

    def save(self, *args, **kwargs):
        # Generar hash antes de guardar si no existe
        if not self.hash_integridad:
            self.hash_integridad = self.generar_hash()
        super().save(*args, **kwargs)

    def verificar_integridad(self):
        """Verifica que el registro no fue alterado."""
        hash_actual = self.hash_integridad
        self.hash_integridad = ''
        hash_calculado = self.generar_hash()
        self.hash_integridad = hash_actual
        return hash_actual == hash_calculado
