import datetime
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from apps.usuarios.models import Medico, Sede, Consultorio
from apps.pacientes.models import Paciente

class EstadoTurno(models.TextChoices):
    PENDIENTE = 'PENDIENTE', 'Pendiente'
    CONFIRMADO = 'CONFIRMADO', 'Confirmado'
    CANCELADO = 'CANCELADO', 'Cancelado'
    ATENDIDO = 'ATENDIDO', 'Atendido'
    AUSENTE = 'AUSENTE', 'Ausente / No asistió'
    EN_ESPERA = 'EN_ESPERA', 'En Sala de Espera'

class Turno(models.Model):
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name='turnos')
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='turnos')
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE, related_name='turnos')
    consultorio = models.ForeignKey(Consultorio, on_delete=models.SET_NULL, null=True, blank=True, related_name='turnos')
    
    fecha = models.DateField()
    hora = models.TimeField()
    duracion_minutos = models.IntegerField(default=30)
    
    estado = models.CharField(
        max_length=20, 
        choices=EstadoTurno.choices, 
        default=EstadoTurno.PENDIENTE
    )
    
    notificado_wsp_medico = models.BooleanField(default=False)
    notificado_wsp_paciente = models.BooleanField(default=False)
    en_lista_espera = models.BooleanField(default=False, help_text="Anotado en lista de espera si se libera un turno")
    
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    notas = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Turno"
        verbose_name_plural = "Turnos"
        ordering = ['fecha', 'hora']

    def __str__(self):
        return f"Turno {self.fecha.strftime('%d/%m/%Y')} {self.hora.strftime('%H:%M')} - {self.paciente.nombre_completo} con {self.medico.nombre_completo}"

    def clean(self):
        super().clean()
        if self.fecha and self.hora and self.medico_id:
            # Calcular rangos de tiempo
            inicio_nuevo = datetime.datetime.combine(self.fecha, self.hora)
            fin_nuevo = inicio_nuevo + datetime.timedelta(minutes=self.duracion_minutos or 30)

            # Buscar turnos existentes para el mismo médico que no estén cancelados
            turnos_existentes = Turno.objects.filter(
                medico_id=self.medico_id,
                fecha=self.fecha
            ).exclude(estado=EstadoTurno.CANCELADO)

            if self.pk:
                turnos_existentes = turnos_existentes.exclude(pk=self.pk)

            for turno in turnos_existentes:
                inicio_existente = datetime.datetime.combine(turno.fecha, turno.hora)
                fin_existente = inicio_existente + datetime.timedelta(minutes=turno.duracion_minutos)

                # Comprobar superposición
                if max(inicio_nuevo, inicio_existente) < min(fin_nuevo, fin_existente):
                    raise ValidationError(
                        f"Superposición de horario: El Dr/a. {self.medico.nombre_completo} ya tiene un turno asignado "
                        f"a las {turno.hora.strftime('%H:%M')} ({turno.paciente.nombre_completo})."
                    )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class FacturaConsulta(models.Model):
    turno = models.OneToOneField(Turno, on_delete=models.CASCADE, related_name='factura')
    tipo_comprobante = models.CharField(max_length=20, blank=True, null=True, help_text="Factura A, B, C (preparado AFIP)")
    cae = models.CharField(max_length=50, blank=True, null=True, help_text="Código de Autorización Electrónico AFIP (preparado)")
    monto = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    fecha_emision = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Factura de Consulta"
        verbose_name_plural = "Facturas de Consulta"

    def __str__(self):
        return f"Factura #{self.id} - Turno #{self.turno_id} (${self.monto})"
