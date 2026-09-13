# SISTEMA DE GESTIÓN DE CONSULTORIOS MÉDICOS

## Documentación Completa - Guía de Despliegue y Configuración

---

## 1. RESUMEN DEL PROYECTO

### ¿Qué es este sistema?
Sistema de gestión profesional para consultorios médicos en Argentina, diseñado para 1 a 10+ médicos. Incluye:

- **Gestión de pacientes** (alta, baja, historial)
- **Agenda de turnos** (con validación de superposición)
- **Historia clínica** (con soft-delete, cumplimiento Ley 26.529)
- **Turnero para sala de espera** (pantalla pública)
- **Panel de recepción** (vista general filtrable)
- **Auditoría de accesos** (trazabilidad completa)
- **Notificaciones WhatsApp** (preparado, pendiente integración)

### Stack Tecnológico
| Componente | Tecnología |
|------------|------------|
| Backend | Python 3 + Django 5.0 |
| Base de datos | PostgreSQL (producción) / SQLite (desarrollo) |
| Frontend | HTML5 + Tailwind CSS (Mobile-first) |
| Servidor | Gunicorn (producción) |
| Archivos estáticos | Whitenoise |
| PDF | ReportLab |

### Estado Actual
- ✅ MVP funcional con 2 médicos de demo
- ✅ CRUD completo de pacientes, médicos, turnos
- ✅ Historia clínica con soft-delete
- ✅ Validación de superposición de turnos
- ✅ Exportación a PDF
- ✅ Vistas mobile-first con Tailwind CSS
- ⏳ Notificaciones WhatsApp (pendiente)
- ⏳ Facturación AFIP (preparado en modelo)

---

## 2. ESTRUCTURA DE LA BASE DE DATOS

### Diagrama de Relaciones

```
USUARIOS (quién atiende)
├── Sede (dónde está el consultorio)
│   └── Consultorio (la sala física)
├── Especialidad (cardiología, pediatría, etc.)
├── Medico (el doctor)
│   └── MedicoSede (dónde y cuándo atiende)

PACIENTES (a quién atiende)
├── ObraSocial (OSDE, Swiss Medical, etc.)
└── Paciente (los datos del paciente)

TURNOS (cuándo)
├── Turno (la cita médica)
└── FacturaConsulta (la factura)

HISTORIA CLÍNICA (qué pasó)
└── HistoriaClinica (notas médicas, diagnóstico)

AUDITORÍA (control)
└── LogAuditoria (quién hizo qué)
```

### Tablas (12 modelos + 1 enum)

| # | Modelo | Tabla | Propósito |
|---|--------|-------|-----------|
| 1 | ConfiguracionSistema | configuracion | Configuración general (singleton) |
| 2 | Sede | usuarios | Sedes/locales del consultorio |
| 3 | Consultorio | usuarios | Salas físicas dentro de cada sede |
| 4 | Especialidad | usuarios | Especialidades médicas |
| 5 | Medico | usuarios | Perfiles de médicos (vinculado a User) |
| 6 | MedicoSede | usuarios | Horarios de atención por sede |
| 7 | ObraSocial | pacientes | Obras sociales |
| 8 | Paciente | pacientes | Registros de pacientes |
| 9 | Turno | turnos | Citas médicas |
| 10 | FacturaConsulta | turnos | Facturas (1:1 con Turno) |
| 11 | HistoriaClinica | historias_clinicas | Registros médicos (soft-delete) |
| 12 | LogAuditoria | auditoria | Registro de auditoría |

### Campos Principales

#### Paciente
- `nombre_completo`, `dni` (unique), `telefono`, `email`
- `fecha_nacimiento`, `numero_afiliado`, `obra_social` (FK)
- `consentimiento_datos`, `consentimiento_fecha`, `consentimiento_ip` (Ley 25.326)
- `proxima_fecha_recall` (para controles periódicos)

#### Medico
- `user` (OneToOne con Django User)
- `nombre_completo`, `matricula_profesional`
- `especialidades` (ManyToMany)
- `telefono_whatsapp`, `activo`
- `google_calendar_id` (preparado para sync futura)

#### Turno
- `medico` (FK), `paciente` (FK), `sede` (FK), `consultorio` (FK)
- `fecha`, `hora`, `duracion_minutos` (default: 30)
- `estado`: PENDIENTE, CONFIRMADO, CANCELADO, ATENDIDO, AUSENTE, EN_ESPERA
- `notificado_wsp_medico`, `notificado_wsp_paciente` (booleanos)
- `en_lista_espera` (para lista de espera automática)

#### HistoriaClinica
- `paciente` (FK), `medico` (FK)
- `fecha_consulta`, `motivo_consulta`, `notas_evolucion`
- `diagnostico`, `tratamiento_prescrito`, `receta_electronica`
- `is_deleted`, `deleted_at` (soft-delete, Ley 26.529)

### Capacidades de la Base de Datos

| Métrica | 2 Médicos | 5 Médicos | 10 Médicos |
|---------|-----------|-----------|------------|
| Turnos/mes | 800 | 2.000 | 4.000 |
| Pacientes nuevos/mes | ~100 | ~250-400 | ~500-800 |
| Historias clínicas/mes | 800 | 2.000 | 4.000 |
| Almacenamiento 1 año | ~100 MB | ~250-300 MB | ~500-600 MB |

---

## 3. MARCO LEGAL ARGENTINO

### Ley 26.529 (Derechos del Paciente e Historia Clínica)
- **Retención obligatoria:** Historias clínicas por 10 años mínimo
- **Soft-Delete:** NUNCA borrado físico `DELETE` (usar `is_deleted=True`)
- **Exportación:** Capacidad de exportación accesible para el paciente en PDF

### Ley 25.326 (Protección de Datos Personales)
- **Consentimiento:** Registro explícito del consentimiento informado
- **Trazabilidad:** Logs de auditoría de accesos
- **Encriptación:** Datos sensibles protegidos

### Cumplimiento en el Sistema
- ✅ Soft-delete en HistoriaClinica (no se borran registros)
- ✅ Consentimiento con checkbox + timestamp + IP
- ✅ Log de auditoría en cada acción relevante
- ✅ Exportación de historia clínica a PDF

---

## 4. USUARIOS DE DEMOSTRACIÓN

### Credenciales después de correr `seed_demo`

| Usuario | Contraseña | Rol |
|---------|------------|-----|
| `admin` | `admin123` | Administrador general |
| `recepcion` | `recepcion123` | Recepcionista |
| `dr.garcia` | `medico123` | Dr. Alejandro García (Cardiología) |
| `dra.martinez` | `medico123` | Dra. Sofía Martínez (Pediatría) |
| `desarrollador` | `dev123` | Desarrollador (acceso técnico) |

---

## 5. OPCIONES DE HOSTING (COMPARATIVA)

### Tabla Comparativa

| Característica | Railway | DonWeb Cloud Server |
|----------------|---------|---------------------|
| **Costo mensual** | $15-20 USD (~$18.000-24.000 ARS) | ~$7.500 ARS |
| **Base de datos** | PostgreSQL incluida | Vos instalás PostgreSQL |
| **Configuración** | Automática (git push) | Manual (SSH) |
| **Soporte** | Comunidad | 24/7 en español |
| **Datos en Argentina** | No (EEUU) | Sí (Rosario) |
| **Facilidad** | Alta | Media |
| **Control** | Limitado | Total |
| **Escalabilidad** | Automática | Manual |

### Recomendación
- **Para empezar rápido y sin complicaciones:** Railway
- **Para tener control total y datos en Argentina:** DonWeb Cloud Server
- **Para escalar con bajo costo:** DonWeb

---

## 6. PLAN DE DESPLIEGUE EN DONWEB

### Requisitos Previos
- Cuenta en DonWeb (donweb.com)
- Conocimientos básicos de SSH/terminal
- Git instalado en tu PC
- Repositorio del código en GitHub

### Paso 1: Crear Cloud Server en DonWeb

1. Ir a [donweb.com](https://donweb.com)
2. Crear cuenta con email y datos de facturación
3. Ir a **Cloud Servers** → **Crear nuevo**
4. Configurar:
   - **Plan:** Starter (2 vCPU, 2 GB RAM, 20 GB SSD)
   - **Sistema operativo:** Ubuntu 22.04 LTS
   - **Región:** Argentina
5. Anotar:
   - IP del servidor
   - Contraseña de root

### Paso 2: Conectar al Servidor

```bash
ssh root@IP_DEL_SERVIDOR
```

Ingresar la contraseña cuando se pida.

### Paso 3: Actualizar e Instalar Dependencias

```bash
# Actualizar sistema
apt update && apt upgrade -y

# Instalar Python, pip, PostgreSQL, Git
apt install python3 python3-pip python3-venv postgresql postgresql-contrib git nginx -y
```

### Paso 4: Configurar Base de Datos PostgreSQL

```bash
# Entrar a PostgreSQL
sudo -u postgres psql

# Crear usuario y base de datos
CREATE USER consultorio WITH PASSWORD 'tu_contraseña_segura';
CREATE DATABASE consultorio_db OWNER consultorio;
GRANT ALL PRIVILEGES ON DATABASE consultorio_db TO consultorio;
\q
```

### Paso 5: Subir el Código

```bash
# Clonar repositorio (si lo subiste a GitHub)
cd /home
git clone https://github.com/TU_USUARIO/consultorios.git
cd consultorios

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### Paso 6: Configurar Variables de Entorno

Crear archivo `.env`:
```bash
nano .env
```

Contenido:
```env
DJANGO_SECRET_KEY=tu_clave_secreta_aqui_cambia_esto
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=TU_IP_O_DOMINIO
DJANGO_CSRF_TRUSTED_ORIGINS=https://TU_IP_O_DOMINIO
DATABASE_URL=postgresql://consultorio:tu_contraseña_segura@localhost/consultorio_db
```

### Paso 7: Correr Migraciones y Datos Demo

```bash
# Activar entorno virtual
source venv/bin/activate

# Correr migraciones
python manage.py migrate

# Cargar datos demo
python manage.py seed_demo
```

### Paso 8: Configurar Nginx

```bash
# Crear configuración de Nginx
nano /etc/nginx/sites-available/consultorios
```

Contenido:
```nginx
server {
    listen 80;
    server_name TU_IP_O_DOMINIO;

    location /static/ {
        alias /home/consultorios/staticfiles/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Activar sitio
ln -s /etc/nginx/sites-available/consultorios /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

### Paso 9: Iniciar el Servidor

```bash
# Crear servicio systemd para que inicie automáticamente
nano /etc/systemd/system/consultorios.service
```

Contenido:
```ini
[Unit]
Description=Consultorios Django App
After=network.target

[Service]
User=root
WorkingDirectory=/home/consultorios
ExecStart=/home/consultorios/venv/bin/gunicorn config.wsgi --bind 127.0.0.1:8000 --workers 3
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Activar e iniciar servicio
systemctl daemon-reload
systemctl enable consultorios
systemctl start consultorios
```

### Paso 10: Configurar Firewall

```bash
# Permitir tráfico HTTP y SSH
ufw allow OpenSSH
ufw allow 'Nginx Full'
ufw enable
```

### Paso 11: Configurar SSL (Opcional pero Recomendado)

```bash
# Instalar Certbot
apt install certbot python3-certbot-nginx -y

# Obtener certificado SSL
certbot --nginx -d TU_DOMINIO
```

---

## 7. VARIABLES DE ENTORNO

### Archivo .env

```env
# Seguridad
DJANGO_SECRET_KEY=tu_clave_secreta_aqui_cambia_esto

# Debug (False en producción)
DJANGO_DEBUG=False

# Hosts permitidos (IP o dominio del servidor)
DJANGO_ALLOWED_HOSTS=192.168.1.100,tu-dominio.com

# CSRF Trusted Origins
DJANGO_CSRF_TRUSTED_ORIGINS=https://192.168.1.100,https://tu-dominio.com

# Base de datos PostgreSQL
DATABASE_URL=postgresql://consultorio:tu_contraseña@localhost/consultorios_db
```

---

## 8. CONFIGURACIÓN PARA 5 MÉDICOS

### Cambiar Límite de Médicos

1. Acceder al panel de administración: `http://TU_IP/admin/`
2. Ir a **Configuraciones del Sistema**
3. Editar `max_medicos_permitidos` de 2 a 5
4. Guardar

### Recursos Necesarios

| Recurso | Mínimo | Recomendado |
|---------|--------|-------------|
| CPU | 2 vCPU | 2 vCPU |
| RAM | 2 GB | 2 GB |
| Almacenamiento | 20 GB | 20 GB |
| Base de datos | 1 GB | 2 GB |

### Costo Estimado

| Concepto | Costo ARS |
|----------|-----------|
| Cloud Server (2 vCPU, 2 GB RAM) | ~$7.500/mes |
| Dominio (opcional) | ~$1.500/año |
| **Total mensual** | **~$7.500** |

---

## 9. ESTRUCTURA DE ARCHIVOS

```
CONSULTORIOS/
├── manage.py
├── requirements.txt
├── Procfile
├── .gitignore
├── .env (no subir a Git)
├── db.sqlite3 (no subir a Git)
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   ├── __init__.py
│   ├── configuracion/      # Configuración del sistema
│   ├── usuarios/           # Sedes, Consultorios, Médicos
│   ├── pacientes/          # Pacientes, Obras Sociales
│   ├── turnos/             # Turnos, Facturas
│   ├── historias_clinicas/ # Historia clínica (soft-delete)
│   ├── auditoria/          # Logs de auditoría
│   └── core/               # Vistas principales, utilidades
├── templates/              # Plantillas HTML5 + Tailwind
│   ├── base.html
│   ├── recepcion/
│   ├── medicos/
│   ├── pacientes/
│   └── turnero/
├── static/                 # CSS/JS estáticos
├── media/                  # Archivos adjuntos / PDFs
└── DOCS/                   # Documentación
    ├── ARQUITECTURA.md
    ├── CONTEXTO_PROYECTO.md
    └── MANUAL_MIGRACION_IA.md
```

---

## 10. COMANDOS ÚTILES

### Desarrollo Local
```bash
# Activar entorno virtual
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate      # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt

# Correr migraciones
python manage.py migrate

# Cargar datos demo
python manage.py seed_demo

# Iniciar servidor de desarrollo
python manage.py runserver 0.0.0.0:8000
```

### Producción (DonWeb)
```bash
# Conectar al servidor
ssh root@IP_DEL_SERVIDOR

# Entrar al directorio del proyecto
cd /home/consultorios

# Activar entorno virtual
source venv/bin/activate

# Correr migraciones
python manage.py migrate

# Cargar datos demo
python manage.py seed_demo

# Reiniciar servicio
systemctl restart consultorios
```

---

## 11. SOLUCIÓN DE PROBLEMAS COMUNES

### Error: "cannot import name 'EMPTY_VALUE_STRING'"
**Causa:** Instalación corrupta de Django
**Solución:**
```bash
pip install --force-reinstall --no-cache-dir Django==5.0.14
```

### Error: "Database connection failed"
**Causa:** PostgreSQL no está corriendo o credenciales incorrectas
**Solución:**
```bash
systemctl status postgresql
systemctl start postgresql
```

### Error: "Static files not found"
**Causa:** No se recolectaron los archivos estáticos
**Solución:**
```bash
python manage.py collectstatic --noinput
```

### Error: "Permission denied"
**Causa:** Permisos incorrectos en archivos
**Solución:**
```bash
chmod -R 755 /home/consultorios
chown -R root:root /home/consultorios
```

---

## 12. PRÓXIMOS PASOS

### Corto Plazo
1. ✅ Documentación completa (este archivo)
2. ⏳ Despliegue en DonWeb
3. ⏳ Configurar dominio personalizado
4. ⏳ Integración WhatsApp (Twilio)

### Mediano Plazo
5. ⏳ Facturación AFIP
6. ⏳ Multi-sede activa
7. ⏳ Receta electrónica

### Largo Plazo
8. ⏳ Portal del Paciente
9. ⏳ App nativa móvil
10. ⏳ Firma digital

---

## 13. CONTACTO Y SOPORTE

### Usuarios de Demo
| Usuario | Contraseña | Rol |
|---------|------------|-----|
| admin | admin123 | Administrador |
| recepcion | recepcion123 | Recepcionista |
| dr.garcia | medico123 | Médico 1 |
| dra.martinez | medico123 | Médico 2 |

### Documentación del Proyecto
- `DOCS/ARQUITECTURA.md` - Arquitectura técnica
- `DOCS/CONTEXTO_PROYECTO.md` - Contexto del proyecto
- `DOCS/MANUAL_MIGRACION_IA.md` - Manual para agentes de IA

---

*Documento generado el 13 de Septiembre de 2026*
*Última actualización: 13 de Septiembre de 2026*
