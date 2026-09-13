# ARQUITECTURA TÉCNICA DEL SISTEMA

## 1. Estructura de Carpetas

```text
CONSULTORIOS/
├── manage.py
├── requirements.txt
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   ├── __init__.py
│   ├── configuracion/      # Ajustes del sistema, cupos de médicos
│   ├── usuarios/           # Sede, Consultorio, Especialidad, Medico, MedicoSede
│   ├── pacientes/          # Paciente, ObraSocial, Consentimientos
│   ├── turnos/             # Turno, Turnero, ListaEspera, Recall
│   ├── historias_clinicas/ # HistoriaClinica, Soft-Delete, PDF
│   ├── auditoria/          # LogAuditoria
│   └── core/               # Comandos de gestión (seed_demo), utilidades
├── templates/              # Vistas HTML5 con Tailwind CSS
│   ├── base.html
│   ├── recepcion/
│   ├── medicos/
│   ├── pacientes/
│   └── turnero/
├── static/                 # CSS/JS estáticos
├── media/                  # Archivos adjuntos / PDFs
└── DOCS/                   # Documentación técnica y funcional
```

---

## 2. Modelo de Licencia / Cupo de Médicos
El sistema incluye el modelo `ConfiguracionSistema`:
- `max_medicos_permitidos`: entero que define el cupo máximo (defecto: 2).
- Al intentar registrar un nuevo médico, el modelo `Medico` ejecuta una validación (`clean()` / `save()`) consultando si el número actual de médicos activos supera `max_medicos_permitidos`. Si la configuración cambia a 10 o a 0 (sin límite), el sistema se adapta automáticamente.

---

## 3. Modelo de Datos Principal

```text
ConfiguracionSistema (Singleton)
 - id
 - nombre_consultorio
 - max_medicos_permitidos (integer, default=2)
 - whatsapp_empresa

Sede -> Consultorio (1 a M)
Especialidad (M a M con Medico)
Medico -> User (1 a 1)
MedicoSede (Medico, Sede, Días, Horarios)

Paciente -> ObraSocial (Nullable)
HistoriaClinica (Paciente, Medico, fecha, notas, is_deleted, deleted_at)
Turno (Medico, Paciente, Sede, fecha, hora, estado, en_lista_espera)
LogAuditoria (User, accion, entidad, entidad_id, timestamp, ip)
```
