import datetime
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from apps.configuracion.models import ConfiguracionSistema
from apps.usuarios.models import Sede, Consultorio, Especialidad, Medico, MedicoSede, PerfilUsuario
from apps.pacientes.models import ObraSocial, Paciente
from apps.turnos.models import Turno, EstadoTurno
from apps.historias_clinicas.models import HistoriaClinica

class Command(BaseCommand):
    help = 'Carga datos iniciales de demostración con 2 Médicos, Especialidades, Pacientes y Turnos de prueba.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Cargando datos de demostración..."))

        # 1. Configuración del sistema
        config = ConfiguracionSistema.get_solo()
        config.nombre_consultorio = "Consultorio Médico San Lucas"
        config.max_medicos_permitidos = 2
        config.modo_demo = True
        config.save()
        self.stdout.write(self.style.SUCCESS("[OK] Configuración del sistema verificada (Cupo: 2 Médicos)"))

        # 2. Usuarios Base
        # 2.1 Usuario Desarrollador (Acceso Exclusivo a Licencia y Cupos)
        if not User.objects.filter(username='desarrollador').exists():
            u_dev = User.objects.create_superuser('desarrollador', 'dev@sistema.com', 'dev123')
            u_dev.first_name = 'Desarrollador'
            u_dev.last_name = 'Sistema'
            u_dev.save()
            PerfilUsuario.objects.create(user=u_dev, rol='DEV')
            self.stdout.write(self.style.SUCCESS("[OK] Usuario Desarrollador Creado: desarrollador / dev123 (Rol: DEV)"))

        # 2.2 Administrador de Clínica
        if not User.objects.filter(username='admin').exists():
            u_admin = User.objects.create_user('admin', 'admin@consultorio.com', 'admin123')
            u_admin.first_name = 'Admin'
            u_admin.last_name = 'Consultorio'
            u_admin.is_staff = True
            u_admin.save()
            PerfilUsuario.objects.create(user=u_admin, rol='ADMIN')
            self.stdout.write(self.style.SUCCESS("[OK] Usuario Admin Clínica creado: admin / admin123 (Rol: ADMIN)"))

        # 2.3 Recepción
        if not User.objects.filter(username='recepcion').exists():
            u_rec = User.objects.create_user('recepcion', 'recepcion@consultorio.com', 'recepcion123')
            u_rec.first_name = 'Recepción'
            u_rec.last_name = 'Central'
            u_rec.is_staff = True
            u_rec.save()
            PerfilUsuario.objects.create(user=u_rec, rol='RECEPCION')
            self.stdout.write(self.style.SUCCESS("[OK] Usuario Recepción creado: recepcion / recepcion123 (Rol: RECEPCION)"))

        # 3. Sedes y Consultorios
        sede, _ = Sede.objects.get_or_create(
            nombre="Sede Central San Lucas",
            defaults={"direccion": "Av. Corrientes 1234, CABA", "telefono": "+54 11 4555-0100", "activa": True}
        )
        cons1, _ = Consultorio.objects.get_or_create(nombre_numero="Consultorio 101 (Cardiología)", sede=sede)
        cons2, _ = Consultorio.objects.get_or_create(nombre_numero="Consultorio 102 (Pediatría)", sede=sede)

        # 4. Especialidades
        esp_cardio, _ = Especialidad.objects.get_or_create(nombre="Cardiología", defaults={"descripcion": "Enfermedades del corazón y sistema circulatorio."})
        esp_pediatria, _ = Especialidad.objects.get_or_create(nombre="Pediatría General", defaults={"descripcion": "Atención médica integral en niños y adolescentes."})
        esp_clinica, _ = Especialidad.objects.get_or_create(nombre="Clínica Médica", defaults={"descripcion": "Atención primaria y medicina interna."})

        # 5. Obras Sociales
        os_osde, _ = ObraSocial.objects.get_or_create(nombre="OSDE 210 / 310 / 410", defaults={"codigo_nomenclador": "OSDE-01"})
        os_swiss, _ = ObraSocial.objects.get_or_create(nombre="Swiss Medical", defaults={"codigo_nomenclador": "SM-02"})
        os_galeno, _ = ObraSocial.objects.get_or_create(nombre="Galeno Argentina", defaults={"codigo_nomenclador": "GAL-03"})
        os_particular, _ = ObraSocial.objects.get_or_create(nombre="Particular / Consulta Privada", defaults={"codigo_nomenclador": "PRIV-00"})

        # 6. Crear Médicos (Límite: 2)
        # Médico 1
        user_med1, _ = User.objects.get_or_create(username='dr.garcia', defaults={'email': 'garcia@consultorio.com', 'first_name': 'Alejandro', 'last_name': 'García', 'is_staff': True})
        if _:
            user_med1.set_password('medico123')
            user_med1.save()
            PerfilUsuario.objects.create(user=user_med1, rol='MEDICO')

        medico1, _ = Medico.objects.get_or_create(
            user=user_med1,
            defaults={
                'nombre_completo': 'Alejandro García',
                'matricula_profesional': 'MN 84512 / MP 45120',
                'telefono_whatsapp': '+5491145678901',
                'activo': True
            }
        )
        medico1.especialidades.add(esp_cardio, esp_clinica)

        # Médico 2
        user_med2, _ = User.objects.get_or_create(username='dra.martinez', defaults={'email': 'martinez@consultorio.com', 'first_name': 'Sofía', 'last_name': 'Martínez', 'is_staff': True})
        if _:
            user_med2.set_password('medico123')
            user_med2.save()
            PerfilUsuario.objects.create(user=user_med2, rol='MEDICO')

        medico2, _ = Medico.objects.get_or_create(
            user=user_med2,
            defaults={
                'nombre_completo': 'Sofía Martínez',
                'matricula_profesional': 'MN 91204 / MP 52103',
                'telefono_whatsapp': '+5491198765432',
                'activo': True
            }
        )
        medico2.especialidades.add(esp_pediatria)

        # Horarios de Atención
        MedicoSede.objects.get_or_create(
            medico=medico1, sede=sede,
            defaults={'dias_atencion': 'Lunes, Miércoles, Viernes', 'horario_inicio': datetime.time(9, 0), 'horario_fin': datetime.time(14, 0), 'duracion_turno_default': 30}
        )
        MedicoSede.objects.get_or_create(
            medico=medico2, sede=sede,
            defaults={'dias_atencion': 'Martes, Jueves', 'horario_inicio': datetime.time(14, 0), 'horario_fin': datetime.time(18, 0), 'duracion_turno_default': 30}
        )
        self.stdout.write(self.style.SUCCESS("[OK] 2 Médicos configurados: Dr. Alejandro García y Dra. Sofía Martínez"))

        # 7. Pacientes
        pacientes_data = [
            {"nombre_completo": "Juan Pablo Gómez", "dni": "35123456", "telefono": "+5491155443322", "email": "jpgomez@gmail.com", "obra_social": os_osde},
            {"nombre_completo": "María Elena Rossi", "dni": "28999888", "telefono": "+5491166778899", "email": "merossi@hotmail.com", "obra_social": os_swiss},
            {"nombre_completo": "Lucas Fernández", "dni": "42111222", "telefono": "+5491133221100", "email": "lucasf@yahoo.com", "obra_social": os_galeno},
            {"nombre_completo": "Lucía Morales", "dni": "38444555", "telefono": "+5491177889900", "email": "luciam@gmail.com", "obra_social": os_particular},
            {"nombre_completo": "Mateo Benítez (Menor)", "dni": "52333444", "telefono": "+5491122334455", "email": "padremateo@gmail.com", "obra_social": os_osde},
        ]

        pacientes = []
        for pdata in pacientes_data:
            p, _ = Paciente.objects.get_or_create(
                dni=pdata["dni"],
                defaults={
                    "nombre_completo": pdata["nombre_completo"],
                    "telefono": pdata["telefono"],
                    "email": pdata["email"],
                    "obra_social": pdata["obra_social"],
                    "consentimiento_datos": True,
                    "consentimiento_ip": "192.168.1.50"
                }
            )
            pacientes.append(p)
        self.stdout.write(self.style.SUCCESS("[OK] 5 Pacientes de prueba creados"))

        # 8. Turnos de prueba para hoy
        hoy = datetime.date.today()
        
        # Turno 1 (Dr. García) - Atendido
        t1, _ = Turno.objects.get_or_create(
            medico=medico1, paciente=pacientes[0], fecha=hoy, hora=datetime.time(9, 0),
            defaults={'sede': sede, 'consultorio': cons1, 'estado': EstadoTurno.ATENDIDO, 'duracion_minutos': 30, 'notas': 'Chequeo de rutina hipertensión.'}
        )

        # Historia Clínica asociada a Turno 1
        HistoriaClinica.objects.get_or_create(
            paciente=pacientes[0], medico=medico1,
            defaults={
                'motivo_consulta': 'Chequeo cardiológico preventivo.',
                'notas_evolucion': 'Presión arterial 125/80 mmHg. Electrocardiograma sin arritmias agudas.',
                'diagnostico': 'Hipertensión arterial controlada.',
                'tratamiento_prescrito': 'Continuar con Enalapril 10mg cada 12hs. Dieta reducida en sodio. Próximo control en 6 meses.'
            }
        )

        # Turno 2 (Dr. García) - En Sala de Espera
        Turno.objects.get_or_create(
            medico=medico1, paciente=pacientes[1], fecha=hoy, hora=datetime.time(9, 30),
            defaults={'sede': sede, 'consultorio': cons1, 'estado': EstadoTurno.EN_ESPERA, 'duracion_minutos': 30}
        )

        # Turno 3 (Dr. García) - Confirmado
        Turno.objects.get_or_create(
            medico=medico1, paciente=pacientes[2], fecha=hoy, hora=datetime.time(10, 0),
            defaults={'sede': sede, 'consultorio': cons1, 'estado': EstadoTurno.CONFIRMADO, 'duracion_minutos': 30}
        )

        # Turno 4 (Dra. Martínez) - Confirmado para la tarde
        Turno.objects.get_or_create(
            medico=medico2, paciente=pacientes[4], fecha=hoy, hora=datetime.time(14, 0),
            defaults={'sede': sede, 'consultorio': cons2, 'estado': EstadoTurno.CONFIRMADO, 'duracion_minutos': 30, 'notas': 'Control pediátrico de 5 años.'}
        )

        self.stdout.write(self.style.SUCCESS("[OK] Turnos de prueba e Historia Clínica inicial creados."))
        self.stdout.write(self.style.SUCCESS("\n========================================================"))
        self.stdout.write(self.style.SUCCESS("  ROLES Y ACCESOS ACTUALIZADOS"))
        self.stdout.write(self.style.SUCCESS("  - DESARROLLADOR (Acceso Total): desarrollador / dev123"))
        self.stdout.write(self.style.SUCCESS("  - ADMIN (Gestión Completa): admin / admin123"))
        self.stdout.write(self.style.SUCCESS("  - RECEPCION (Turnos y Pacientes): recepcion / recepcion123"))
        self.stdout.write(self.style.SUCCESS("  - MEDICO (Agenda y HC): dr.garcia / medico123"))
        self.stdout.write(self.style.SUCCESS("  - MEDICO (Agenda y HC): dra.martinez / medico123"))
        self.stdout.write(self.style.SUCCESS("========================================================\n"))
