from django.db import models

class ObraSocial(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    codigo_nomenclador = models.CharField(max_length=50, blank=True, null=True, help_text="Código nomenclador nacional (preparado)")

    class Meta:
        verbose_name = "Obra Social / Prepaga"
        verbose_name_plural = "Obras Sociales / Prepagas"

    def __str__(self):
        return self.nombre

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
    consentimiento_datos = models.BooleanField(default=True, help_text="Consentimiento de tratamiento de datos según Ley 25.326")
    consentimiento_fecha = models.DateTimeField(auto_now_add=True)
    consentimiento_ip = models.GenericIPAddressField(default="127.0.0.1")
    
    # Recall de controles periódicos (🟢 Construir ya)
    proxima_fecha_recall = models.DateField(blank=True, null=True, help_text="Fecha sugerida para el próximo control médico preventivo")

    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"

    def __str__(self):
        return f"{self.nombre_completo} (DNI: {self.dni})"
