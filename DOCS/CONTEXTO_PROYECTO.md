# CONTEXTO MAESTRO DEL PROYECTO: SISTEMA DE GESTIÓN DE CONSULTORIOS

## 1. Visión General
Sistema de gestión profesional para consultorio médico en Argentina (adaptable a 1 a 10+ médicos), diseñado para ser el producto de mayor calidad dentro de su categoría: prolijo, seguro, legalmente conforme con las leyes argentinas y con una UX/UI excepcional.

### Estado Inicial de Demo:
- Precargado para **2 Médicos** para demostraciones a clientes y profesionales.
- Módulo de configuración de sistema (`ConfiguracionSistema`) con parámetro `max_medicos_permitidos` (defecto: 2 en demo, configurable fácilmente a 10 o ilimitado).

---

## 2. Marco Legal Argentino
- **Ley 26.529 (Derechos del Paciente e Historia Clínica):**
  - Retención obligatoria de historias clínicas por 10 años mínimo.
  - Implementación de **Soft-Delete** (NUNCA borrado físico `DELETE`).
  - Capacidad de exportación accesible para el paciente en PDF.
- **Ley 25.326 (Protección de Datos Personales):**
  - Registro explícito del consentimiento informado (Checkbox + Timestamp + IP de registro).
  - Encriptación de datos sensibles y trazabilidad de accesos mediante logs de auditoría.

---

## 3. Stack Tecnológico
- **Backend:** Python 3 + Django
- **Base de Datos:** PostgreSQL (o SQLite en entorno de desarrollo local)
- **Frontend:** HTML5 + Tailwind CSS (Mobile-first, responsive, tipografía Inter/Outfit)
- **Mensajería:** Twilio WhatsApp Business API + Sistema de Notificaciones In-App de contingencia
- **Autenticación:** Django Auth + 2FA (django-otp)

---

## 4. Clasificación de Funcionalidades
- 🟢 **CONSTRUIR YA (MVP Ampliado):**
  1. CRUD Pacientes, Médicos, Especialidades, Horarios.
  2. Agenda de turnos con validación de superposición.
  3. Historia clínica con notas, diagnóstico, tratamiento y Soft-Delete.
  4. Panel de recepción general filtrable.
  5. Vista de médico mobile-first (2 toques).
  6. Notificaciones WhatsApp e In-App.
  7. Turnero para sala de espera en tiempo real.
  8. Lista de espera automática por cancelaciones.
  9. Recall de controles periódicos.
  10. Auditoría de accesos e historial de cambios.
  11. Exportación de Historia Clínica a PDF.
- 🟡 **PREPARADO EN MODELO DE DATOS:**
  - Facturación AFIP, Obras Sociales, Receta Electrónica, Multi-sede activa.
- ⚪ **BACKLOG FUTURO:**
  - Portal del Paciente, Firma Digital, Mercado Pago, App Nativa, Multi-tenant.
