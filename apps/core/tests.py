import datetime
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from apps.configuracion.models import ConfiguracionSistema
from apps.usuarios.models import Sede, Consultorio, Especialidad, Medico
from apps.pacientes.models import Paciente
from apps.turnos.models import Turno, EstadoTurno
from apps.historias_clinicas.models import HistoriaClinica

class ConsultorioTestCase(TestCase):
    def setUp(self):
        # Configuración sistema con cupo de 2 médicos
        self.config = ConfiguracionSistema.get_solo()
        self.config.max_medicos_permitidos = 2
        self.config.save()

        self.sede = Sede.objects.create(nombre="Sede Test", direccion="Calle Test 123")
        self.esp = Especialidad.objects.create(nombre="Cardiología Test")

        # Crear Médico 1
        u1 = User.objects.create_user('m1', 'm1@test.com', 'pass')
        self.medico1 = Medico.objects.create(
            user=u1, nombre_completo="Médico 1", matricula_profesional="M1", 
            telefono_whatsapp="+5491100000001", activo=True
        )
        self.medico1.especialidades.add(self.esp)

        # Crear Médico 2
        u2 = User.objects.create_user('m2', 'm2@test.com', 'pass')
        self.medico2 = Medico.objects.create(
            user=u2, nombre_completo="Médico 2", matricula_profesional="M2", 
            telefono_whatsapp="+5491100000002", activo=True
        )
        self.medico2.especialidades.add(self.esp)

        # Paciente
        self.paciente = Paciente.objects.create(nombre_completo="Paciente Test", dni="11223344", telefono="+5491100000000")

    def test_limite_medicos_activos(self):
        """Verifica que el sistema impida registrar un 3er médico activo cuando el cupo es 2."""
        u3 = User.objects.create_user('m3', 'm3@test.com', 'pass')
        medico3 = Medico(
            user=u3, nombre_completo="Médico 3", matricula_profesional="M3", 
            telefono_whatsapp="+5491100000003", activo=True
        )
        
        with self.assertRaises(ValidationError):
            medico3.save()

    def test_superposicion_turnos(self):
        """Verifica que no se permitan turnos superpuestos para el mismo médico."""
        hoy = datetime.date.today()
        # Turno 1 de 10:00 a 10:30
        Turno.objects.create(
            medico=self.medico1, paciente=self.paciente, sede=self.sede,
            fecha=hoy, hora=datetime.time(10, 0), duracion_minutos=30, estado=EstadoTurno.CONFIRMADO
        )

        # Intento de Turno 2 superpuesto (10:15)
        turno2 = Turno(
            medico=self.medico1, paciente=self.paciente, sede=self.sede,
            fecha=hoy, hora=datetime.time(10, 15), duracion_minutos=30, estado=EstadoTurno.CONFIRMADO
        )
        with self.assertRaises(ValidationError):
            turno2.save()

    def test_soft_delete_historia_clinica(self):
        """Verifica el cumplimiento de Ley 26.529: borrado lógico de Historia Clínica."""
        hc = HistoriaClinica.objects.create(
            paciente=self.paciente,
            medico=self.medico1,
            motivo_consulta="Prueba",
            diagnostico="Diagnóstico Test"
        )
        self.assertEqual(HistoriaClinica.objects.count(), 1)
        
        # Eliminar
        hc.delete()

        # No debe aparecer en objects.all() pero sí en all_with_deleted
        self.assertEqual(HistoriaClinica.objects.count(), 0)
        self.assertEqual(HistoriaClinica.all_with_deleted.count(), 1)
        self.assertTrue(HistoriaClinica.all_with_deleted.first().is_deleted)
