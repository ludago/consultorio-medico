from django.db import models
from django.utils import timezone


class ObraSocial(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    codigo_nomenclador = models.CharField(max_length=50, blank=True, null=True, help_text="Código nomenclador nacional (preparado)")

    class Meta:
        verbose_name = "Obra Social / Prepaga"
        verbose_name_plural = "Obras Sociales / Prepagas"

    def __str__(self):
        return self.nombre


class PacienteQuerySet(models.QuerySet):
    def activos(self):
        return self.filter(is_deleted=False)

    def eliminados(self):
        return self.filter(is_deleted=True)


class PacienteManager(models.Manager):
    def get_queryset(self):
        return PacienteQuerySet(self.model, using=self._db).filter(is_deleted=False)

    def eliminados(self):
        return PacienteQuerySet(self.model, using=self._db).filter(is_deleted=True)

    def todos_incluyendo_eliminados(self):
        return PacienteQuerySet(self.model, using=self._db)


class Paciente(models.Model):
    nombre_completo = models.CharField(max_length=200)
    dni = models.CharField(max_length=20, unique=True, help_text="DNI / Documento de Identidad")
    telefono = models.CharField(max_length=50, help_text="Número móvil para recordatorios por WhatsApp (ej: +5491112345678)")
    email = models.EmailField(blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    obra_social = models.ForeignKey(ObraSocial, on_delete=models.SET_NULL, null=True, blank=True, related_name='pacientes', help_text="Obra social o prepaga (preparado)")
    numero_afiliado = models.CharField(max_length=100, blank=True, null=True, help_text="Número de credencial/afiliado (preparado)")
    datos_contacto_adicionales = models.TextField(blank=True, help_text="Contacto de emergencia, tutor o allegado")

    # Ley 25.326 - Consentimiento informado de datos personales
    consentimiento_datos = models.BooleanField(default=False, help_text="Consentimiento de tratamiento de datos según Ley 25.326")
    consentimiento_fecha = models.DateTimeField(blank=True, null=True)
    consentimiento_ip = models.GenericIPAddressField(blank=True, null=True)

    # Recall de controles periódicos
    proxima_fecha_recall = models.DateField(blank=True, null=True, help_text="Fecha sugerida para el próximo control médico preventivo")

    fecha_registro = models.DateTimeField(auto_now_add=True)

    # Soft-delete Ley 26.529 (Retención 10 años mínimo)
    is_deleted = models.BooleanField(default=False, help_text="Marca de borrado lógico para auditoría y cumplimiento legal")
    deleted_at = models.DateTimeField(blank=True, null=True)

    objects = PacienteManager()
    all_with_deleted = models.Manager()

    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"

    def __str__(self):
        return f"{self.nombre_completo} (DNI: {self.dni})"

    def delete(self, using=None, keep_parents=False):
        """Soft delete según Ley 26.529"""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(using=using)
