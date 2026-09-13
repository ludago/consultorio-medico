# MANUAL DE MIGRACIÓN Y CONTINUIDAD PARA AGENTES DE IA

> [!NOTE]
> Este documento permite a cualquier agente de IA (o desarrollador) retomar este proyecto inmediatamente sin requerir re-explicaciones por parte del usuario.

## 1. Comandos de Inicio Rápido

```bash
# 1. Crear entorno virtual (si no existe)
python -m venv venv

# 2. Activar entorno virtual
# En Windows PowerShell:
.\venv\Scripts\Activate.ps1

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Aplicar migraciones de base de datos
python manage.py migrate

# 5. Cargar datos de demostración (2 Médicos, Especialidades, Pacientes, Turnos de prueba)
python manage.py seed_demo

# 6. Iniciar servidor de desarrollo local
python manage.py runserver
```

---

## 2. Usuarios Predeterminados Creados por `seed_demo`

| Usuario | Contraseña | Rol / Descripción |
|---|---|---|
| `admin` | `admin123` | Administrador general / Recepción |
| `recepcion` | `recepcion123` | Usuario Recepcionista |
| `dr.garcia` | `medico123` | Médico 1: Dr. Alejandro García (Cardiología) |
| `dra.martinez` | `medico123` | Médico 2: Dra. Sofía Martínez (Pediatría) |

---

## 3. Modificación del Cupo Máximo de Médicos
Para cambiar el límite de médicos permitidos en el sistema:
1. Acceder al panel de administración Django `/admin`.
2. Ir a **Configuraciones del Sistema**.
3. Editar `max_medicos_permitidos` (por ejemplo, cambiar de `2` a `10` o `0` para sin límite).

---

## 4. Convenciones del Proyecto
- **Soft-Delete obligatorio:** En `apps.historias_clinicas`, nunca eliminar registros de la base de datos física (`is_deleted=True`).
- **Mobile-First:** Todas las plantillas HTML en `templates/` utilizan clases responsivas de Tailwind CSS.
- **Validación de Turnos:** La función de validación de superposición en `apps.turnos` debe ser invocada tanto en admin como en vistas públicas.
