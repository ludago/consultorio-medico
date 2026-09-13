# AUDITORÍA COMPLETA DEL SISTEMA DE CONSULTORIOS

## Análisis de Seguridad, Calidad y Preparación para Producción

**Fecha:** 13 de Septiembre de 2026
**Resultado:** 47 problemas encontrados (6 Críticos, 11 Altos, 14 Medios, 16 Bajos)
**Veredicto:** NECESITA CORRECCIONES ANTES DE VENDER

---

## RESUMEN EJECUTIVO

| Severidad | Cantidad | Estado |
|-----------|----------|--------|
| **Críticos** | 6 | SIN ESTO NO SE PUEDE VENDER |
| **Altos** | 11 | DEBEN RESOLVERSE PRONTO |
| **Medios** | 14 | AFECTAN CALIDAD PROFESIONAL |
| **Bajos** | 16 | MEJORAS PENDIENTES |
| **TOTAL** | **47** | |

### Top 5 - Lo PRIMERO que hay que arreglar:

1. **Seguridad de Credenciales** - Ocultar credenciales de demo, contraseñas fuertes
2. **Control de Roles y Permisos** - Médicos solo ven SUS pacientes
3. **Headers de Seguridad** - Forzar HTTPS, cookies seguras
4. **Formularios con Validación** - Django Forms para cada formulario
5. **Consentimiento Real** - Checkbox explícito con timestamp e IP real

---

## PROBLEMAS CRÍTICOS (6) - Sin esto NO podés vender

### C1. SECRET_KEY Hardcodeada (Insegura)

**Archivo:** `config/settings.py` línea 6

**Problema:**
```python
SECRET_KEY = 'django-insecure-consultorio-medico-demo-key-super-secret-123456'
```

**Riesgo:** Si alguien descubre esta clave, puede:
- Robar sesiones de usuarios
- Forjar tokens CSRF
- Tomar control de cuentas

**Solución:**
- Usar variable de entorno `DJANGO_SECRET_KEY`
- Generar una clave aleatoria de 50+ caracteres
- NUNCA commitear la clave al repositorio

---

### C2. Credenciales de Demo Visibles en Login

**Archivo:** `templates/registration/login.html` líneas 58-72

**Problema:** La página de login muestra permanentemente:
```
dr.garcia / medico123
dra.martinez / medico123
recepcion / recepcion123
```

**Riesgo:** Cualquiera que entre a la página puede loguearse como médico o admin.

**Solución:**
- Mostrar credenciales SOLO si `modo_demo=True` en ConfiguracionSistema
- En producción, nunca mostrar contraseñas

---

### C3. Contraseñas Débiles en Demo

**Archivo:** `apps/core/management/commands/seed_demo.py`

**Problema:** Todas las contraseñas son triviales:
- `admin123`
- `medico123`
- `recepcion123`
- `dev123`

**Riesgo:** Fuerza bruta trivial, acceso no autorizado.

**Solución:**
- En modo demo: mantener contraseñas débiles (es intencional)
- En producción: FORZAR cambio de contraseña en primer login
- Agregar validación de contraseñas fuertes

---

### C4. Sin Control de Roles y Permisos

**Archivo:** `apps/core/views.py`

**Problema:** Cualquier usuario logueado puede:
- Ver historias clínicas de CUALQUIER paciente (línea 109)
- Crear registros médicos sin ser médico (línea 123)
- Cambiar estado de CUALquier turno (línea 86)
- Ver agenda de CUALQUIER médico (línea 65)

**Riesgo:** **Violación directa de Ley 26.529** - Un recepcionista puede ver y modificar historias clínicas.

**Solución:**
- Implementar `@permission_required` o decoradores personalizados
- Médicos: solo ven SUS pacientes y turnos
- Recepcionistas: solo ven turnos, NO historias clínicas
- Admin: solo superuser

---

### C5. SQLite como Base por Defecto

**Archivo:** `config/settings.py` líneas 63-68

**Problema:** La configuración por defecto usa SQLite:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

**Riesgo:**
- Se corrompe con varios usuarios concurrentes
- No soporta conexiones de red
- No tiene control de acceso a nivel base de datos

**Solución:**
- PostgreSQL como base por defecto en producción
- SQLite SOLO para desarrollo local
- Documentar claramente la configuración

---

### C6. db.sqlite3 con Datos Sensibles en Repositorio

**Archivo:** `db.sqlite3` en la raíz del proyecto

**Problema:** El archivo contiene datos reales de pacientes:
- Nombres, DNI, teléfonos
- Historias clínicas
- Datos de contacto

**Riesgo:** Fuga de datos sensibles si el repositorio es público o es hackeado.

**Solución:**
- Eliminar `db.sqlite3` del repositorio
- Agregar a `.gitignore`
- Nunca commitear base de datos con datos reales
- Si ya se commiteó, limpiar el historial de Git

---

## PROBLEMAS ALTOS (11) - Deben resolverse pronto

### H1. Turnero Público Expone Datos de Pacientes

**Archivo:** `apps/core/views.py` líneas 157-179

**Problema:** `turnero_pantalla()` no tiene `@login_required` y muestra:
- Nombres completos de pacientes
- Nombres de médicos
- Horarios de citas

**Riesgo:** Cualquiera con la URL puede ver quién está visitando al médico.

**Solución:**
- Ocultar nombres completos (mostrar solo iniciales o "Paciente X")
- O exigir autenticación para acceder

---

### H2. Sin Headers de Seguridad

**Archivo:** `config/settings.py`

**Problema:** No están configurados:
- `SECURE_SSL_REDIRECT` (no fuerza HTTPS)
- `SESSION_COOKIE_SECURE` (cookies por HTTP)
- `CSRF_COOKIE_SECURE` (CSRF por HTTP)
- `SECURE_HSTS_SECONDS` (sin HSTS)
- `SECURE_CONTENT_TYPE_NOSNIFF`

**Riesgo:** Ataques MITM, robo de sesiones, clickjacking.

**Solución:** Agregar todas las configuraciones de seguridad en settings.py para producción.

---

### H3. ALLOWED_HOSTS con Wildcard

**Archivo:** `config/settings.py` línea 10

**Problema:** `ALLOWED_HOSTS = ['*']`

**Riesgo:** Inyección de headers HTTP, ataques de DNS rebinding.

**Solución:** Especificar DOMINIOS EXACTOS en producción:
```python
ALLOWED_HOSTS = ['consultorios.com', 'www.consultorios.com']
```

---

### H5. Admin Panel Accesible para Todos los Staff

**Archivo:** `config/urls.py` línea 7

**Problema:** Cualquier usuario con `is_staff=True` puede acceder al admin y ver/modify:
- Todos los pacientes
- Todas las historias clínicas
- Todos los logs de auditoría
- La configuración del sistema

**Riesgo:** Un recepcionista puede borrar pacientes o modificar configuración.

**Solución:**
- Restringir admin solo a `is_superuser=True`
- O crear permisos personalizados por modelo

---

### H6. Sin Validación en Formularios Médicos

**Archivo:** `apps/core/views.py` líneas 123-149

**Problema:** Los formularios usan `request.POST.get()` sin validación:
```python
motivo = request.POST.get('motivo_consulta')
diagnostico = request.POST.get('diagnostico')
```

**Riesgo:**
- Campos vacíos en historias clínicas
- Datos basura
- XSS almacenado

**Solución:** Crear Django Forms con validación para cada formulario.

---

### H7. No Se Usan Django Forms

**Archivo:** Todos los directorios `apps/*/forms.py` (no existen)

**Problema:** Ninguna app tiene `forms.py`. Todo usa HTML raw con `request.POST.get()`.

**Riesgo:**
- Sin validación server-side
- Sin renderizado automático
- Sin protección CSRF de doble submit
- Sin sanitización de inputs

**Solución:** Crear `forms.py` en cada app con ModelForm o Form personalizado.

---

### H9. Consultas N+1 en Dashboard

**Archivo:** `templates/recepcion/dashboard.html` línea 139

**Problema:**
```html
{% for esp in t.medico.especialidades.all %}
```
Dispara una consulta por cada turno para obtener las especialidades.

**Riesgo:** Lento con muchos turnos (O(N) queries).

**Solución:** Agregar `prefetch_related('medico__especialidades')` al queryset de turnos.

---

### H10. Sin Configuración de Logging

**Archivo:** `config/settings.py`

**Problema:** No existe configuración `LOGGING`.

**Riesgo:** Imposible debugear, detectar ataques, o auditar en producción.

**Solución:** Configurar logging a archivo o servicio de logs.

---

### H11. Servicio WhatsApp Incompleto

**Archivo:** `apps/core/services/whatsapp.py`

**Problemas:**
- Usa `print()` en modo fallback (no funciona en producción)
- `twilio` no está en `requirements.txt`
- Sin manejo de errores

**Riesgo:** Notificaciones no funcionan, dependencia faltante.

**Solución:**
- Agregar `twilio` a requirements.txt
- Implementar logging en vez de print()
- Agregar manejo de errores y reintentos

---

## PROBLEMAS MEDIOS (14) - Afectan calidad profesional

### M1. Sin Favicon
**Problema:** No hay `favicon.ico` ni configuración en `base.html`.
**Impacto:** Errores 404 en cada carga, poco profesional.

### M2. Sin Páginas de Error (404, 500)
**Problema:** No existen `404.html` ni `500.html`.
**Impacto:** Django muestra páginas por defecto con detalles técnicos.

### M3. Tailwind CSS vía CDN
**Problema:** Usa `cdn.tailwindcss.com` (no recomendado para producción).
**Impacto:** Lento (~100KB JS extra), no cacheable.

### M4. Font Awesome vía CDN Externo
**Problema:** Depende de `cdnjs.cloudflare.com`.
**Impacto:** Si el CDN cae, se pierden todos los iconos.

### M5. Google Fonts vía CDN
**Problema:** Depende de `fonts.googleapis.com`.
**Impacto:** Google recibe IPs de visitantes (riesgo privacidad).

### M6. URLs Hardcodeadas en Templates
**Problema:** URLs como `/admin/` hardcodeadas en templates.
**Impacto:** Se rompen si cambian las rutas.

### M7. Consentimiento Automático (No Real)
**Problema:** `consentimiento_datos` default=True, `consentimiento_fecha` auto_now_add.
**Impacto:** **No cumple Ley 25.326** - El consentimiento debe ser explícito.

### M8. Logs de Auditoría Incompletos
**Problema:** Falta: HTTP method, URL, user agent, valores before/after.
**Impacto:** Sin capacidad forense para auditorías médicas.

### M10. Sin Rate Limiting en Login
**Problema:** No hay protección contra fuerza bruta.
**Impacto:** Atacantes pueden probar contraseñas ilimitadamente.

### M11. Sin Configuración de Seguridad de Sesiones
**Problema:** Cookies enviadas por HTTP, sin SameSite explícito.
**Impacto:** Robo de sesiones.

### M12. Solo 3 Tests Básicos
**Problema:** Solo hay tests de: límite médico, superposición turnos, soft-delete.
**Impacto:** Sin red de seguridad, sin regresión.

### M13. Admin Sin Personalizar
**Problema:** Admin registrations mínimos, sin fieldsets ni readonly_fields.
**Impacto:** Mala UX para administradores.

### M14. FacturaConsulta es Stub
**Problema:** Modelo existe pero no tiene integración AFIP real.
**Impacto:** Producto incompleto, capacidades engañosas.

---

## PROBLEMAS BAJOS (16) - Mejoras pendientes

| # | Problema | Impacto |
|---|----------|---------|
| L1 | Sin archivos estáticos locales (todo CDN) | Sin offline capability |
| L2 | `STATICFILES_STORAGE` deprecado en Django 4.2+ | Warnings, posible rotura |
| L3 | Sin configuración LOGGING | Sin observabilidad |
| L4 | `medico_agenda` sin selector de fecha | No puede ver turnos futuros |
| L5 | Sin paginación en listados | Lento con muchos registros |
| L6 | Sin estados de carga (AJAX) | UX deficiente |
| L7 | `consentimiento_ip` hardcodeada a 127.0.0.1 | Auditoría inválida |
| L8 | Sin validación de transiciones de estado | Estados imposibles |
| L9 | Open redirect en `cambiar_estado_turno` | Seguridad |
| L10 | `Medico.clean()` bypass via admin | Límite evadido |
| L11 | Sin menú móvil responsive | UX rota en móvil |
| L12 | `django-otp` instalado pero no usado | 2FA no implementado |
| L13 | `django-cors-headers` sin configurar | Dependencia inútil |
| L14 | `dias_atencion` en texto libre | No se puede consultar disponibilidad |
| L15 | Sin exportación de datos | Brecha cumplimiento |
| L16 | `consentimiento_fecha` auto_now_add | Historial inmutable |

---

## PLAN DE CORRECCIÓN

### Fase 1: Críticos (2-3 horas)

| # | Tarea | Tiempo |
|---|-------|--------|
| C1 | Generar SECRET_KEY segura + variable de entorno | 15 min |
| C2 | Modo demo condicional (ocultar credenciales) | 30 min |
| C3 | Validación de contraseñas + forced reset | 30 min |
| C4 | Control de roles (permisos por vista) | 60 min |
| C5 | PostgreSQL como default producción | 15 min |
| C6 | Eliminar db.sqlite3 del repo | 5 min |

### Fase 2: Altos (4-6 horas)

| # | Tarea | Tiempo |
|---|-------|--------|
| H1 | Ocultar datos en turnero | 30 min |
| H2 | Headers de seguridad | 30 min |
| H3 | ALLOWED_HOSTS específico | 10 min |
| H5 | Restringir admin panel | 30 min |
| H6+H7 | Django Forms para todos los formularios | 120 min |
| H9 | Optimizar queries N+1 | 30 min |
| H10 | Configurar logging | 30 min |
| H11 | Arreglar servicio WhatsApp | 30 min |

### Fase 3: Medios (6-8 horas)

| # | Tarea | Tiempo |
|---|-------|--------|
| M1 | Agregar favicon | 10 min |
| M2 | Crear 404.html y 500.html | 30 min |
| M3 | Compilar Tailwind CSS localmente | 60 min |
| M4 | Font Awesome local | 30 min |
| M5 | Google Fonts local | 30 min |
| M6 | URLs con template tags | 30 min |
| M7 | Consentimiento real con checkbox | 60 min |
| M8 | Auditoría completa | 60 min |
| M10 | Rate limiting (django-ratelimit) | 30 min |
| M11 | Seguridad de sesiones | 15 min |
| M12 | Tests básicos | 120 min |
| M13 | Admin personalizado | 60 min |
| M14 | Stub de FacturaConsulta (advertencia) | 15 min |

### Fase 4: Bajos (horas libres)

| # | Tarea | Tiempo |
|---|-------|--------|
| L1-L6 | Estáticos locales, paginación, AJAX | 3-4 horas |
| L7-L11 | Consentimiento IP, transiciones, menú móvil | 2-3 horas |
| L12-L16 | 2FA, CORS, exportación, etc. | 3-4 horas |

---

## CHECKLIST ANTES DE VENDER

### Seguridad
- [ ] SECRET_KEY en variable de entorno (no hardcodeada)
- [ ] Credenciales de demo ocultas en producción
- [ ] Contraseñas fuertes obligatorias
- [ ] Control de roles implementado
- [ ] HTTPS forzado
- [ ] Cookies seguras (Secure, HttpOnly, SameSite)
- [ ] Rate limiting en login
- [ ] Admin restringido a superuser

### Cumplimiento Legal
- [ ] Consentimiento explícito con checkbox
- [ ] Timestamp e IP real del consentimiento
- [ ] Soft-delete en historias clínicas
- [ ] Auditoría completa (quién, qué, cuándo, desde dónde)
- [ ] Retención de 10 años documentada

### Calidad
- [ ] Django Forms en todos los formularios
- [ ] Validación de datos médicos
- [ ] Sin consultas N+1
- [ ] Logging configurado
- [ ] Tests mínimos (10+ casos)
- [ ] Páginas de error personalizadas
- [ ] Favicon y branding

### Despliegue
- [ ] .gitignore completo (sin db.sqlite3)
- [ ] Variables de entorno documentadas
- [ ] Instrucciones de deploy claras
- [ ] Backup automático configurado

---

## COMANDOS ÚTILES PARA CORRECCIONES

### Generar SECRET_KEY segura
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Crear superuser con contraseña fuerte
```bash
python manage.py createsuperuser
```

### Correr tests
```bash
python manage.py test
```

### Verificar seguridad
```bash
python manage.py check --deploy
```

---

## NOTA FINAL

El sistema tiene una **buena arquitectura base** y **cumple parcialmente** con las leyes argentinas. Los problemas encontrados son **solucionables** y no requieren reescribir el sistema.

**Tiempo estimado total de corrección:** 12-18 horas

**Prioridad:** Arreglar los 6 críticos ANTES de vender. Los altos se pueden ir arreglando iterativamente.

---

*Documento generado el 13 de Septiembre de 2026*
*Última actualización: 13 de Septiembre de 2026*
