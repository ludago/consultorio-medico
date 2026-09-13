#!/usr/bin/env python
"""
Genera un PDF completo con la información del Sistema de Gestión de Consultorio Médico.
"""
from fpdf import FPDF
import os

class ConsultorioPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=20)

    def header(self):
        self.set_font('Helvetica', 'B', 9)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, 'Sistema de Gestión de Consultorio Médico - Documentación Completa', align='C', new_x="LMARGIN", new_y="NEXT")
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(3)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f'Página {self.page_no()}/{{nb}}', align='C')

    def titulo_seccion(self, texto):
        self.set_font('Helvetica', 'B', 14)
        self.set_text_color(0, 102, 178)
        self.ln(4)
        self.cell(0, 10, texto, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(0, 102, 178)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(3)

    def sub_seccion(self, texto):
        self.set_font('Helvetica', 'B', 11)
        self.set_text_color(50, 50, 50)
        self.ln(2)
        self.cell(0, 8, texto, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def texto(self, texto):
        self.set_font('Helvetica', '', 10)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 5.5, texto)
        self.ln(1)

    def tabla(self, headers, data, col_widths=None):
        if col_widths is None:
            col_widths = [190 / len(headers)] * len(headers)
        
        # Header
        self.set_font('Helvetica', 'B', 9)
        self.set_fill_color(0, 102, 178)
        self.set_text_color(255, 255, 255)
        for i, h in enumerate(headers):
            self.cell(col_widths[i], 7, h, border=1, fill=True, align='C')
        self.ln()

        # Data
        self.set_font('Helvetica', '', 8)
        self.set_text_color(30, 30, 30)
        fill = False
        for row in data:
            if self.get_y() > 265:
                self.add_page()
            if fill:
                self.set_fill_color(235, 245, 255)
            else:
                self.set_fill_color(255, 255, 255)
            
            max_lines = 1
            cell_texts = []
            for i, cell in enumerate(row):
                text = str(cell)
                # Calcular líneas necesarias
                lines = max(1, len(text) // int(col_widths[i] / 2.2) + 1)
                max_lines = max(max_lines, lines)
                cell_texts.append(text)
            
            row_h = max(7, max_lines * 5)
            
            y_before = self.get_y()
            x_before = self.get_x()
            
            for i, text in enumerate(cell_texts):
                self.set_xy(x_before + sum(col_widths[:i]), y_before)
                self.multi_cell(col_widths[i], 5, text, border=1, fill=fill, align='L', max_line_height=5)
            
            self.set_xy(x_before, y_before + row_h)
            fill = not fill
        self.ln(2)

    def item_lista(self, texto):
        self.set_font('Helvetica', '', 10)
        self.set_text_color(30, 30, 30)
        x = self.get_x()
        self.cell(8, 5.5, '-', new_x="END")
        self.multi_cell(170, 5.5, texto)


def generar_pdf():
    pdf = ConsultorioPDF()
    pdf.alias_nb_pages()
    pdf.set_margins(15, 15, 15)

    # ============================================================
    # PORTADA
    # ============================================================
    pdf.add_page()
    pdf.ln(30)
    pdf.set_font('Helvetica', 'B', 28)
    pdf.set_text_color(0, 102, 178)
    pdf.cell(0, 15, 'Sistema de Gestion', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 15, 'de Consultorio Medico', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(8)
    pdf.set_font('Helvetica', '', 16)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 10, 'Documentacion Completa del Sistema', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    pdf.set_draw_color(0, 102, 178)
    pdf.set_line_width(1)
    pdf.line(60, pdf.get_y(), 150, pdf.get_y())
    pdf.ln(15)

    pdf.set_font('Helvetica', '', 12)
    pdf.set_text_color(60, 60, 60)

    info_portada = [
        ('Framework:', 'Django (Python)'),
        ('Frontend:', 'HTML5 + Tailwind CSS (CDN)'),
        ('Base de datos:', 'SQLite3 (dev) / PostgreSQL (produccion)'),
        ('Ley 25.326:', 'Consentimiento de datos personales'),
        ('Ley 26.529:', 'Historia clinica - Retencion 10 anios'),
        ('Ubicacion:', 'C:\\Users\\User\\Desktop\\IA_developer\\CONSULTORIOS'),
    ]

    for label, valor in info_portada:
        pdf.set_font('Helvetica', 'B', 11)
        pdf.cell(55, 8, label, align='R')
        pdf.set_font('Helvetica', '', 11)
        pdf.cell(0, 8, '  ' + valor, new_x="LMARGIN", new_y="NEXT")

    # ============================================================
    # 1. ARQUITECTURA DEL SISTEMA
    # ============================================================
    pdf.add_page()
    pdf.titulo_seccion('1. ARQUITECTURA DEL SISTEMA')

    pdf.sub_seccion('1.1 Stack Tecnologico')
    pdf.tabla(
        ['Componente', 'Tecnologia', 'Version/Detalle'],
        [
            ['Backend', 'Django (Python)', '>=4.2, <5.1'],
            ['Frontend', 'HTML5 + Tailwind CSS', 'CDN (sin framework JS)'],
            ['BD Desarrollo', 'SQLite3', 'db.sqlite3'],
            ['BD Produccion', 'PostgreSQL', 'via dj-database-url'],
            ['Servidor WSGI', 'Gunicorn', '>=21.2.0'],
            ['Estilos', 'Tailwind CSS + Font Awesome', 'CDN'],
            ['Fuentes', 'Google Fonts Inter', 'CDN'],
        ],
        [40, 50, 100]
    )

    pdf.sub_seccion('1.2 Dependencias (requirements.txt)')
    pdf.tabla(
        ['Paquete', 'Version', 'Uso'],
        [
            ['Django', '>=4.2, <5.1', 'Framework web principal'],
            ['Pillow', '>=10.0.0', 'Manejo de imagenes'],
            ['django-otp', '>=1.3.0', 'Autenticacion OTP (preparado)'],
            ['qrcode', '>=7.4.2', 'Generacion de QR codes'],
            ['reportlab', '>=4.0.0', 'Generacion de PDFs'],
            ['django-cors-headers', '>=4.3.0', 'Headers CORS'],
            ['gunicorn', '>=21.2.0', 'Servidor WSGI produccion'],
            ['whitenoise', '>=6.5.0', 'Archivos estaticos'],
            ['dj-database-url', '>=2.1.0', 'URL BD variable entorno'],
        ],
        [45, 35, 110]
    )

    pdf.sub_seccion('1.3 Estructura de Carpetas')
    estructura = """CONSULTORIOS/
  manage.py                    - CLI de Django
  requirements.txt             - Dependencias Python
  Procfile                     - Despliegue Heroku/Render
  db.sqlite3                   - Base de datos SQLite (dev)
  generar_pdf_propuesta.py     - Generador PDF comercial
  config/                      - Configuracion del proyecto Django
    settings.py                - Settings principales
    urls.py                    - URL router principal
    wsgi.py / asgi.py          - Puntos de entrada WSGI/ASGI
  apps/                        - Aplicaciones de dominio
    configuracion/             - ConfiguracionSistema (singleton)
    usuarios/                  - Sedes, Consultorios, Medicos, Especialidades
    pacientes/                 - Pacientes y Obras Sociales
    turnos/                    - Turnos y Facturacion
    historias_clinicas/        - Historia clinica (soft-delete)
    auditoria/                 - Log de auditoria
    core/                      - Vistas principales + servicios
  templates/                   - Templates HTML5
    base.html                  - Layout base
    registration/login.html    - Login
    recepcion/dashboard.html   - Panel recepcion
    medicos/agenda.html        - Agenda medica
    pacientes/                 - Historia clinica
    turnero/pantalla.html      - Turnero Smart TV
  static/                      - Archivos estaticos (CDN)
  DOCS/                        - Documentacion del proyecto"""
    pdf.texto(estructura)

    # ============================================================
    # 2. MODELO DE DATOS
    # ============================================================
    pdf.add_page()
    pdf.titulo_seccion('2. MODELO DE DATOS (12 modelos)')

    pdf.sub_seccion('2.1 ConfiguracionSistema (app: configuracion)')
    pdf.tabla(
        ['Campo', 'Tipo', 'Detalle'],
        [
            ['nombre_consultorio', 'CharField(200)', 'Default: "Consultorio Medico San Lucas"'],
            ['max_medicos_permitidos', 'IntegerField', 'Default: 2 (cupo licencia)'],
            ['telefono_whatsapp_empresa', 'CharField(50)', 'Numero WhatsApp empresa'],
            ['direccion_consultorio', 'CharField(300)', 'Direccion fisica'],
            ['modo_demo', 'BooleanField', 'True = modo demostracion'],
            ['fecha_actualizacion', 'DateTimeField', 'auto_now'],
        ],
        [55, 40, 95]
    )
    pdf.texto('Metodo get_solo() - Patron Singleton: crea o retorna la unica instancia (id=1).')

    pdf.sub_seccion('2.2 Sede (app: usuarios)')
    pdf.tabla(
        ['Campo', 'Tipo', 'Detalle'],
        [
            ['nombre', 'CharField(150)', 'Nombre de la sede'],
            ['direccion', 'CharField(250)', 'Direccion fisica'],
            ['telefono', 'CharField(50)', 'Telefono de contacto'],
            ['activa', 'BooleanField', 'Si la sede esta operativa'],
        ],
        [40, 40, 110]
    )

    pdf.sub_seccion('2.3 Consultorio (app: usuarios)')
    pdf.tabla(
        ['Campo', 'Tipo', 'Detalle'],
        [
            ['nombre_numero', 'CharField(100)', 'Ej: "Consultorio 102 - Planta Alta"'],
            ['sede', 'FK -> Sede', 'Relacion 1 a M con Sede'],
        ],
        [40, 40, 110]
    )

    pdf.sub_seccion('2.4 Especialidad (app: usuarios)')
    pdf.tabla(
        ['Campo', 'Tipo', 'Detalle'],
        [
            ['nombre', 'CharField(150)', 'Unico. Ej: Cardiologia, Pediatria'],
            ['descripcion', 'TextField', 'Descripcion opcional'],
        ],
        [40, 40, 110]
    )

    pdf.sub_seccion('2.5 Medico (app: usuarios)')
    pdf.tabla(
        ['Campo', 'Tipo', 'Detalle'],
        [
            ['user', 'OneToOne -> User', 'Vinculado 1:1 a User de Django'],
            ['nombre_completo', 'CharField(200)', 'Nombre completo del medico'],
            ['matricula_profesional', 'CharField(50)', 'Matricula Nacional o Provincial'],
            ['especialidades', 'MME -> Especialidad', 'Relacion M a M'],
            ['telefono_whatsapp', 'CharField(50)', 'Con codigo de pais (+549...)'],
            ['activo', 'BooleanField', 'Si esta activo en el sistema'],
            ['google_calendar_id', 'CharField(255)', 'Preparado para sync futura'],
        ],
        [45, 40, 105]
    )
    pdf.texto('Validacion clean(): respeta el cupo max_medicos_permitidos de ConfiguracionSistema. Si se alcanza el limite, lanza ValidationError.')

    pdf.add_page()
    pdf.sub_seccion('2.6 MedicoSede (app: usuarios)')
    pdf.tabla(
        ['Campo', 'Tipo', 'Detalle'],
        [
            ['medico', 'FK -> Medico', 'Medico que atiende'],
            ['sede', 'FK -> Sede', 'Sede donde atiende'],
            ['dias_atencion', 'CharField(100)', '"Lunes, Miercoles, Viernes"'],
            ['horario_inicio', 'TimeField', 'Hora de inicio'],
            ['horario_fin', 'TimeField', 'Hora de fin'],
            ['duracion_turno_default', 'IntegerField', 'Default: 30 min'],
        ],
        [45, 40, 105]
    )

    pdf.sub_seccion('2.7 Paciente (app: pacientes)')
    pdf.tabla(
        ['Campo', 'Tipo', 'Detalle'],
        [
            ['nombre_completo', 'CharField(200)', 'Nombre completo'],
            ['dni', 'CharField(20)', 'Unico - Documento de Identidad'],
            ['telefono', 'CharField(50)', 'Movil para WhatsApp'],
            ['email', 'EmailField', 'Email opcional'],
            ['fecha_nacimiento', 'DateField', 'Fecha de nacimiento'],
            ['obra_social', 'FK -> ObraSocial', 'Obra social/prepaga'],
            ['numero_afiliado', 'CharField(100)', 'Credencial de afiliado'],
            ['datos_contacto_adicionales', 'TextField', 'Contacto de emergencia'],
            ['consentimiento_datos', 'BooleanField', 'Ley 25.326 (default True)'],
            ['consentimiento_fecha', 'DateTimeField', 'auto_now_add'],
            ['consentimiento_ip', 'GenericIPAddressField', 'IP de consentimiento'],
            ['proxima_fecha_recall', 'DateField', 'Proximo control preventivo'],
            ['fecha_registro', 'DateTimeField', 'auto_now_add'],
        ],
        [50, 40, 100]
    )

    pdf.sub_seccion('2.8 ObraSocial (app: pacientes)')
    pdf.tabla(
        ['Campo', 'Tipo', 'Detalle'],
        [
            ['nombre', 'CharField(200)', 'Unico - Nombre de la obra social'],
            ['codigo_nomenclador', 'CharField(50)', 'Codigo nomenclador nacional'],
        ],
        [50, 40, 100]
    )

    pdf.sub_seccion('2.9 Turno (app: turnos)')
    pdf.tabla(
        ['Campo', 'Tipo', 'Detalle'],
        [
            ['medico', 'FK -> Medico', 'Medico asignado'],
            ['paciente', 'FK -> Paciente', 'Paciente que solicita'],
            ['sede', 'FK -> Sede', 'Sede del turno'],
            ['consultorio', 'FK -> Consultorio', 'Sala fisica (opcional)'],
            ['fecha', 'DateField', 'Fecha del turno'],
            ['hora', 'TimeField', 'Hora del turno'],
            ['duracion_minutos', 'IntegerField', 'Default: 30 min'],
            ['estado', 'CharField(20)', 'Estados: PENDIENTE, CONFIRMADO, CANCELADO, ATENDIDO, AUSENTE, EN_ESPERA'],
            ['notificado_wsp_medico', 'BooleanField', 'Notificacion WhatsApp enviada'],
            ['notificado_wsp_paciente', 'BooleanField', 'Notificacion WhatsApp enviada'],
            ['en_lista_espera', 'BooleanField', 'En lista de espera'],
            ['creado_por', 'FK -> User', 'Usuario que creo el turno'],
            ['notas', 'TextField', 'Notas adicionales'],
            ['fecha_creacion', 'DateTimeField', 'auto_now_add'],
        ],
        [50, 40, 100]
    )

    pdf.add_page()
    pdf.sub_seccion('2.10 FacturaConsulta (app: turnos)')
    pdf.tabla(
        ['Campo', 'Tipo', 'Detalle'],
        [
            ['turno', 'OneToOne -> Turno', 'Factura vinculada al turno'],
            ['tipo_comprobante', 'CharField(20)', 'Factura A, B, C (AFIP)'],
            ['cae', 'CharField(50)', 'Codigo Autorizacion Electronica AFIP'],
            ['monto', 'DecimalField(12,2)', 'Monto de la consulta'],
            ['fecha_emision', 'DateTimeField', 'auto_now_add'],
        ],
        [45, 40, 105]
    )

    pdf.sub_seccion('2.11 HistoriaClinica (app: historias_clinicas)')
    pdf.tabla(
        ['Campo', 'Tipo', 'Detalle'],
        [
            ['paciente', 'FK -> Paciente', 'Paciente de la consulta'],
            ['medico', 'FK -> Medico', 'Medico que atendio (RESTRICT)'],
            ['fecha_consulta', 'DateTimeField', 'Fecha y hora de la consulta'],
            ['motivo_consulta', 'TextField', 'Motivo reportado por paciente'],
            ['notas_evolucion', 'TextField', 'Examen fisico y observaciones'],
            ['diagnostico', 'TextField', 'Diagnostico o hipotesis'],
            ['tratamiento_prescrito', 'TextField', 'Indicaciones medicas'],
            ['receta_electronica', 'TextField', 'Preparado para receta digital'],
            ['is_deleted', 'BooleanField', 'Soft-delete (Ley 26.529)'],
            ['deleted_at', 'DateTimeField', 'Fecha de borrado logico'],
        ],
        [45, 40, 105]
    )
    pdf.texto('Soft-delete: El manager por defecto (objects) solo muestra registros activos. all_with_deleted muestra todos. delete() marca is_deleted=True en vez de borrar fisicamente. Cumple Ley 26.529: retencion minima 10 anios.')

    pdf.sub_seccion('2.12 LogAuditoria (app: auditoria)')
    pdf.tabla(
        ['Campo', 'Tipo', 'Detalle'],
        [
            ['usuario', 'FK -> User', 'Usuario que realizo la accion'],
            ['accion', 'CharField(50)', 'CREAR / EDITAR / ELIMINAR / VER / EXPORTAR'],
            ['entidad', 'CharField(100)', 'Ej: HistoriaClinica, Paciente, Turno'],
            ['entidad_id', 'CharField(50)', 'ID del registro afectado'],
            ['detalles', 'TextField', 'Descripcion de la accion'],
            ['timestamp', 'DateTimeField', 'auto_now_add'],
            ['ip_origen', 'GenericIPAddressField', 'IP del usuario'],
        ],
        [40, 40, 110]
    )

    # ============================================================
    # 3. VISTAS Y URLS
    # ============================================================
    pdf.add_page()
    pdf.titulo_seccion('3. VISTAS Y URLS')

    pdf.sub_seccion('3.1 Rutas Principales')
    pdf.tabla(
        ['URL', 'Vista', 'Funcionalidad', 'Auth'],
        [
            ['/', 'home_redirect', 'Redirige segun perfil del usuario', 'No'],
            ['/admin/', 'Django Admin', 'Panel de administracion', 'Staff'],
            ['/accounts/login/', 'LoginView', 'Formulario de login', 'No'],
            ['/accounts/logout/', 'LogoutView', 'Cerrar sesion', 'No'],
            ['/recepcion/', 'recepcion_dashboard', 'Dashboard recepcion con KPIs', 'Si'],
            ['/medico/agenda/', 'medico_agenda', 'Agenda mobile del medico', 'Si'],
            ['/turnos/<id>/cambiar-estado/', 'cambiar_estado_turno', 'POST cambiar estado', 'Si'],
            ['/pacientes/<id>/historia-clinica/', 'paciente_historia_clinica', 'Ver/crear HC', 'Si'],
            ['/turnero/', 'turnero_pantalla', 'Pantalla Smart TV sala espera', 'No'],
        ],
        [45, 38, 65, 15]
    )

    pdf.sub_seccion('3.2 Vista: recepcion_dashboard')
    pdf.texto('Dashboard multi-medico para recepcion. Filtra turnos por fecha y medico. Muestra KPIs (total, en espera, confirmados, atendidos, cancelados), tabla de turnos con acciones rapidas ("Anunciar Llegada", "HC").')

    pdf.sub_seccion('3.3 Vista: medico_agenda')
    pdf.texto('Agenda mobile-first del medico. Muestra cards de turnos del dia con botones "Iniciar/Atendido" e "Historia Clinica". Si el usuario no es medico pero es staff, accede al agenda del primer medico activo.')

    pdf.sub_seccion('3.4 Vista: turnero_pantalla')
    pdf.texto('Pantalla publica para Smart TV en sala de espera. Auto-refresh cada 10 segundos. Muestra reloj en vivo, pacientes llamados (verde), lista de espera. No requiere autenticacion.')

    pdf.sub_seccion('3.5 Vista: paciente_historia_clinica')
    pdf.texto('Muestra historial clinico del paciente + formulario para nueva evolucion medica. Registra auditoria de acceso (Ley 26.529).')

    pdf.sub_seccion('3.6 Vista: cambiar_estado_turno')
    pdf.texto('Endpoint POST para cambiar estado de un turno. Registra cambio en LogAuditoria con usuario, accion, entidad y IP.')

    # ============================================================
    # 4. FUNCIONALIDADES
    # ============================================================
    pdf.add_page()
    pdf.titulo_seccion('4. FUNCIONALIDADES IMPLEMENTADAS')

    funcionalidades = [
        ('Panel de Recepcion', 'Dashboard completo con filtros por fecha/medico, estadisticas en tiempo real y acciones rapidas (anunciar llegada, ver HC).'),
        ('Agenda Mobile del Medico', 'Vista mobile-first con tarjetas de turnos, 1 toque para cambiar estado. Iniciar, Atendido, Historia Clinica.'),
        ('Turnero TV Sala de Espera', 'Pantalla publica para Smart TV con reloj en vivo, pacientes llamados en verde, auto-refresh cada 10 segundos.'),
        ('Historia Clinica Legal', 'Formulario de evolucion medica + timeline historica + soft-delete obligatorio (Ley 26.529, retencion 10 anios).'),
        ('Validacion de Superposicion', 'El modelo Turno valida que no haya dos turnos simultaneos para el mismo medico en la misma fecha/hora.'),
        ('Regla de Cupo/Licencia', 'ConfiguracionSistema limita la cantidad de medicos activos (default: 2). Validacion en clean() del modelo Medico.'),
        ('Auditoria Completa', 'LogAuditoria registra cada cambio de estado de turno y cada acceso a historia clinica con usuario, IP y timestamp.'),
        ('WhatsApp (Twilio)', 'Servicio preparado en apps/core/services/whatsapp.py para enviar notificaciones. Simula en modo demo.'),
        ('Seed de Demostracion', 'Comando "python manage.py seed_demo" que carga: 2 medicos, 5 pacientes, 4 turnos, 1 historia clinica.'),
        ('Sistema de Login', '5 usuarios demo con roles: desarrollador (superuser), admin, recepcion, dr.garcia (medico), dra.martinez (medico).'),
        ('Cumplimiento Legal', 'Ley 25.326 (consentimiento datos personales) y Ley 26.529 (historia clinica con retencion minima 10 anios).'),
        ('Diseno Dark Mode', 'UI oscura (slate-950) con glassmorphism, paleta medica (cyan/blue), Tailwind CSS via CDN.'),
    ]

    for titulo, desc in funcionalidades:
        pdf.set_font('Helvetica', 'B', 10)
        pdf.set_text_color(0, 102, 178)
        pdf.cell(5, 6, '>', new_x="END")
        pdf.cell(0, 6, ' ' + titulo, new_x="LMARGIN", new_y="NEXT")
        pdf.set_font('Helvetica', '', 9)
        pdf.set_text_color(50, 50, 50)
        pdf.multi_cell(0, 5, '   ' + desc)
        pdf.ln(2)

    # ============================================================
    # 5. FUNCIONALIDADES PENDIENTES
    # ============================================================
    pdf.add_page()
    pdf.titulo_seccion('5. FUNCIONALIDADES PREPARADAS (Pendientes)')

    pendientes = [
        ('Facturacion AFIP', 'Modelo FacturaConsulta preparado con tipo comprobante A/B/C y campo CAE. Falta integrar con AFIP.'),
        ('Obras Sociales', 'Modelo ObraSocial con codigo nomenclador. Falta validacion de afiliados y nomenclador.'),
        ('Receta Electronica', 'Campo receta_electronica en HistoriaClinica. Falta generacion y envio digital.'),
        ('Google Calendar Sync', 'Campo google_calendar_id en Medico. Falta integracion con Google Calendar API.'),
        ('QR Codes', 'Libreria qrcode instalada. Pendiente generacion de QR para turnos o pacientes.'),
        ('django-otp', 'Libreria instalada para autenticacion de dos factores. Pendiente integracion.'),
    ]

    for titulo, desc in pendientes:
        pdf.set_font('Helvetica', 'B', 10)
        pdf.set_text_color(200, 150, 0)
        pdf.cell(5, 6, '>', new_x="END")
        pdf.cell(0, 6, ' ' + titulo, new_x="LMARGIN", new_y="NEXT")
        pdf.set_font('Helvetica', '', 9)
        pdf.set_text_color(50, 50, 50)
        pdf.multi_cell(0, 5, '   ' + desc)
        pdf.ln(2)

    # ============================================================
    # 6. CREDENCIALES DE DEMO
    # ============================================================
    pdf.titulo_seccion('6. CREDENCIALES DE DEMOSTRACION')
    pdf.tabla(
        ['Usuario', 'Contrasena', 'Rol', 'Nombre'],
        [
            ['desarrollador', 'dev123', 'Superusuario', 'Acceso total (licencia/cupos)'],
            ['admin', 'admin123', 'Administrador', 'Staff de clinica'],
            ['recepcion', 'recepcion123', 'Recepcion', 'Staff de recepcion'],
            ['dr.garcia', 'medico123', 'Medico', 'Dr. Alejandro Garcia - Cardiologia'],
            ['dra.martinez', 'medico123', 'Medico', 'Dra. Sofia Martinez - Pediatria'],
        ],
        [30, 28, 30, 102]
    )

    # ============================================================
    # 7. FLUJOS DE USUARIO
    # ============================================================
    pdf.add_page()
    pdf.titulo_seccion('7. FLUJOS DE USUARIO')

    pdf.sub_seccion('7.1 Flujo de Login')
    pdf.texto('1. Usuario accede a /accounts/login/\n2. Ingresa usuario y contrasena\n3. Django autentica contra User model\n4. home_redirect redirige segun perfil:\n   - Si es medico -> /medico/agenda/\n   - Si es recepcion/admin -> /recepcion/')

    pdf.sub_seccion('7.2 Flujo de Turno (Recepcion)')
    pdf.texto('1. Recepcion selecciona fecha y medico\n2. Ve KPIs: total, en espera, confirmados, atendidos, cancelados\n3. Tabla de turnos con acciones:\n   - "Anunciar Llegada" -> estado = EN_ESPERA\n   - "HC" -> Redirige a historia clinica del paciente\n4. Cambio de estado registra en LogAuditoria')

    pdf.sub_seccion('7.3 Flujo de Atencion (Medico)')
    pdf.texto('1. Medico ve agenda del dia en mobile\n2. Cards de turnos con estado actual\n3. Botones de accion:\n   - "Iniciar" -> estado = EN_ESPERA\n   - "Atendido" -> estado = ATENDIDO\n   - "Historia Clinica" -> Formulario de evolucion\n4. Creacion de HC registra en LogAuditoria')

    pdf.sub_seccion('7.4 Flujo Turnero TV')
    pdf.texto('1. Smart TV accede a /turnero/ (sin login)\n2. Muestra reloj en vivo\n3. Pacientes en EN_ESPERA o CONFIRMADO se muestran en lista\n4. Pacientes en ATENDIDO se muestran como "Siendo atendidos"\n5. Auto-refresh cada 10 segundos')

    pdf.sub_seccion('7.5 Flujo Historia Clinica')
    pdf.texto('1. Desde recepcion o agenda del medico\n2. Se accede a /pacientes/<id>/historia-clinica/\n3. Se registra acceso en LogAuditoria (Ley 26.529)\n4. Se muestra timeline de consultas anteriores\n5. Formulario para nueva evolucion:\n   - Motivo de consulta\n   - Diagnostico\n   - Notas de evolucion\n   - Tratamiento prescrito\n6. Se guarda y se registra creacion en LogAuditoria')

    # ============================================================
    # 8. SEGURIDAD Y CUMPLIMIENTO LEGAL
    # ============================================================
    pdf.add_page()
    pdf.titulo_seccion('8. SEGURIDAD Y CUMPLIMIENTO LEGAL')

    pdf.sub_seccion('8.1 Seguridad')
    seg_items = [
        'CSRF activado en todas las vistas de formulario',
        'Login required en todas las vistas sensibles',
        'Auditoria completa de accesos y acciones',
        'Soft-delete para historia clinica (no borrado fisico)',
        'Validacion de superposicion de turnos',
        'Cupo maximo de medicos por licencia',
        'WhiteNoise con compresion y manifest para estaticos',
    ]
    for item in seg_items:
        pdf.item_lista(item)

    pdf.sub_seccion('8.2 Ley 25.326 - Datos Personales')
    pdf.texto('Consentimiento informado de tratamiento de datos personales. Campo consentimiento_datos en Paciente con timestamp e IP de registro.')

    pdf.sub_seccion('8.3 Ley 26.529 - Historia Clinica')
    pdf.texto('Retencion minima de 10 anios de historia clinica. Implementacion via soft-delete (is_deleted + deleted_at). Custom Manager que filtra registros activos por defecto. All_with_deleted para acceso administrativo.')

    # ============================================================
    # 9. DESPLIEGUE
    # ============================================================
    pdf.titulo_seccion('9. DESPLIEGUE')
    pdf.sub_seccion('9.1 Desarrollo Local')
    pdf.texto("""1. Crear entorno virtual: python -m venv venv
2. Activar: venv\\Scripts\\activate (Windows)
3. Instalar dependencias: pip install -r requirements.txt
4. Migraciones: python manage.py migrate
5. Datos demo: python manage.py seed_demo
6. Crear superuser: python manage.py createsuperuser
7. Ejecutar: python manage.py runserver
8. Acceder a http://127.0.0.1:8000/""")

    pdf.sub_seccion('9.2 Produccion (Heroku/Render)')
    pdf.texto("""1. Configurar variable de entorno DATABASE_URL (PostgreSQL)
2. Configurar DJANGO_SECRET_KEY
3. Configurar DJANGO_DEBUG=False
4. El Procfile ejecuta: gunicorn config.wsgi
5. WhiteNoise sirve archivos estaticos
6. python manage.py collectstatic""")

    # ============================================================
    # 10. COMANDOS UTILES
    # ============================================================
    pdf.add_page()
    pdf.titulo_seccion('10. COMANDOS UTILES')
    pdf.tabla(
        ['Comando', 'Descripcion'],
        [
            ['python manage.py runserver', 'Iniciar servidor de desarrollo'],
            ['python manage.py migrate', 'Aplicar migraciones a la BD'],
            ['python manage.py seed_demo', 'Cargar datos de demostracion'],
            ['python manage.py createsuperuser', 'Crear superusuario'],
            ['python manage.py collectstatic', 'Recopilar archivos estaticos'],
            ['python manage.py shell', 'Shell interactiva de Django'],
            ['python manage.py test', 'Ejecutar tests'],
            ['python manage.py dbshell', 'Consola de la base de datos'],
        ],
        [85, 105]
    )

    # ============================================================
    # GUARDAR
    # ============================================================
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Documentacion_Consultorio_Medico.pdf')
    pdf.output(output_path)
    print(f"PDF generado exitosamente: {output_path}")
    return output_path


if __name__ == '__main__':
    generar_pdf()
