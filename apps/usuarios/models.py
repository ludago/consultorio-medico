from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from apps.configuracion.models import ConfiguracionSistema

class Sede(models.Model):
    nombre = models.CharField(max_length=150)
    direccion = models.CharField(max_length=250)
    telefono = models.CharField(max_length=50, blank=True)
    activa = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Sede"
        verbose_name_plural = "Sedes"

    def __str__(self):
        return self.nombre

class Consultorio(models.Model):
    nombre_numero = models.CharField(max_length=100, help_text="Ej: Consultorio 102 - Planta Alta")
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE, related_name='consultorios')

    class Meta:
        verbose_name = "Consultorio (Sala Física)"
        verbose_name_plural = "Consultorios (Salas Físicas)"

    def __str__(self):
        return f"{self.nombre_numero} ({self.sede.nombre})"

class Especialidad(models.Model):
    nombre = models.CharField(max_length=150, unique=True)
    descripcion = models.TextField(blank=True)

    class Meta:
        verbose_name = "Especialidad Médica"
        verbose_name_plural = "Especialidades Médicas"

    def __str__(self):
        return self.nombre

class Medico(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil_medico')
    nombre_completo = models.CharField(max_length=200)
    matricula_profesional = models.CharField(max_length=50, help_text="Matrícula Nacional o Provincial")
    especialidades = models.ManyToManyField(Especialidad, related_name='medicos')
    telefono_whatsapp = models.CharField(max_length=50, help_text="Número con código de país (ej: +5491112345678)")
    activo = models.BooleanField(default=True)
    google_calendar_id = models.CharField(max_length=255, blank=True, null=True, help_text="Preparado para sync futura")

    class Meta:
        verbose_name = "Médico"
        verbose_name_plural = "Médicos"

    def __str__(self):
        especialidades_str = ", ".join([e.nombre for e in self.especialidades.all()]) if self.pk else ""
        return f"Dr/a. {self.nombre_completo} ({especialidades_str or 'Sin Especialidad'})"

    def clean(self):
        super().clean()
        if self.activo:
            config = ConfiguracionSistema.get_solo()
            limite = config.max_medicos_permitidos
            if limite > 0:
                qs = Medico.objects.filter(activo=True)
                if self.pk:
                    qs = qs.exclude(pk=self.pk)
                if qs.count() >= limite:
                    raise ValidationError(
                        f"No se puede activar/crear el médico. Se ha alcanzado el límite de {limite} médicos activos "
                        f"permitidos por la configuración actual del sistema (Demo/Licencia). "
                        f"Actualice el cupo en 'Configuraciones del Sistema' para permitir más médicos."
                    )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class MedicoSede(models.Model):
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name='horarios_sede')
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE, related_name='horarios_medicos')
    dias_atencion = models.CharField(max_length=100, help_text="Ej: Lunes, Miércoles, Viernes")
    horario_inicio = models.TimeField()
    horario_fin = models.TimeField()
    duracion_turno_default = models.IntegerField(default=30, help_text="Duración estándar del turno en minutos")

    class Meta:
        verbose_name = "Horario de Atención por Sede"
        verbose_name_plural = "Horarios de Atención por Sede"

    def __str__(self):
        return f"{self.medico.nombre_completo} - {self.sede.nombre} ({self.dias_atencion} {self.horario_inicio.strftime('%H:%M')} a {self.horario_fin.strftime('%H:%M')})"
