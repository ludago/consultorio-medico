from django.db import models

class ConfiguracionSistema(models.Model):
    nombre_consultorio = models.CharField(
        max_length=200, 
        default="Consultorio Médico San Lucas"
    )
    max_medicos_permitidos = models.IntegerField(
        default=2, 
        help_text="Cupo máximo de médicos habilitados. Cambiar a 10 o a 0 (sin límite) según la licencia."
    )
    telefono_whatsapp_empresa = models.CharField(
        max_length=50, 
        blank=True, 
        default="+5491100000000"
    )
    direccion_consultorio = models.CharField(
        max_length=300, 
        blank=True, 
        default="Av. Corrientes 1234, CABA, Argentina"
    )
    modo_demo = models.BooleanField(
        default=True, 
        help_text="Indica si el sistema está operando en modo demostración con datos iniciales de prueba."
    )
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Configuración del Sistema"
        verbose_name_plural = "Configuraciones del Sistema"

    def __str__(self):
        limite = "Sin Límite" if self.max_medicos_permitidos == 0 else f"{self.max_medicos_permitidos} Médicos"
        return f"{self.nombre_consultorio} (Cupo: {limite})"

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(id=1)
        return obj
