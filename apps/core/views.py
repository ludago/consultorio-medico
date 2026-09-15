import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.utils import timezone
from django.db.models import Q

from apps.configuracion.models import ConfiguracionSistema
from apps.usuarios.models import Medico, Especialidad, Sede, Consultorio
from apps.pacientes.models import Paciente
from apps.turnos.models import Turno, EstadoTurno
from apps.historias_clinicas.models import HistoriaClinica
from apps.auditoria.models import LogAuditoria
from .decorators import role_required, get_user_role


def home_redirect(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')
    
    user_role = get_user_role(request.user)
    
    # Redirigir segun el rol del usuario
    if user_role == 'MEDICO' or hasattr(request.user, 'perfil_medico'):
        return redirect('medico_agenda')
    elif user_role in ['RECEPCION', 'ADMIN', 'DEV']:
        return redirect('recepcion_dashboard')
    else:
        return redirect('recepcion_dashboard')


@login_required
@role_required(['RECEPCION', 'ADMIN', 'DEV'])
def recepcion_dashboard(request):
    config = ConfiguracionSistema.get_solo()
    fecha_str = request.GET.get('fecha')
    if fecha_str:
        try:
            fecha_sel = datetime.datetime.strptime(fecha_str, '%Y-%m-%d').date()
        except ValueError:
            fecha_sel = datetime.date.today()
    else:
        fecha_sel = datetime.date.today()

    medico_id = request.GET.get('medico')
    
    turnos_qs = Turno.objects.filter(fecha=fecha_sel).select_related('medico', 'paciente', 'consultorio')
    if medico_id:
        turnos_qs = turnos_qs.filter(medico_id=medico_id)

    medicos = Medico.objects.filter(activo=True).prefetch_related('especialidades')
    
    # Estadísticas para el header del dashboard
    stats = {
        'total': turnos_qs.count(),
        'en_espera': turnos_qs.filter(estado=EstadoTurno.EN_ESPERA).count(),
        'confirmados': turnos_qs.filter(estado=EstadoTurno.CONFIRMADO).count(),
        'atendidos': turnos_qs.filter(estado=EstadoTurno.ATENDIDO).count(),
        'cancelados': turnos_qs.filter(estado=EstadoTurno.CANCELADO).count(),
    }

    context = {
        'config': config,
        'fecha_sel': fecha_sel,
        'medico_sel_id': int(medico_id) if medico_id else None,
        'medicos': medicos,
        'turnos': turnos_qs,
        'stats': stats,
        'estados': EstadoTurno.choices,
    }
    return render(request, 'recepcion/dashboard.html', context)


@login_required
@role_required(['RECEPCION', 'ADMIN', 'DEV'])
def nuevo_turno(request):
    medicos = Medico.objects.filter(activo=True).prefetch_related('especialidades')
    pacientes = Paciente.objects.all().order_by('nombre_completo')
    sedes = Sede.objects.filter(activa=True)
    consultorios = Consultorio.objects.all().select_related('sede')

    if request.method == 'POST':
        medico_id = request.POST.get('medico')
        paciente_id = request.POST.get('paciente')
        sede_id = request.POST.get('sede')
        consultorio_id = request.POST.get('consultorio')
        fecha_str = request.POST.get('fecha')
        hora_str = request.POST.get('hora')
        duracion = request.POST.get('duracion', 30)
        notas = request.POST.get('notas', '')

        nuevo_paciente = request.POST.get('nuevo_paciente')
        if nuevo_paciente == '1':
            nombre = request.POST.get('nuevo_nombre', '').strip()
            dni = request.POST.get('nuevo_dni', '').strip()
            tel = request.POST.get('nuevo_telefono', '').strip()
            if nombre and dni and tel:
                paciente = Paciente.objects.create(
                    nombre_completo=nombre,
                    dni=dni,
                    telefono=tel,
                )
                paciente_id = paciente.id

        if medico_id and paciente_id and fecha_str and hora_str:
            try:
                fecha = datetime.datetime.strptime(fecha_str, '%Y-%m-%d').date()
                hora = datetime.datetime.strptime(hora_str, '%H:%M').time()

                turno = Turno(
                    medico_id=int(medico_id),
                    paciente_id=int(paciente_id),
                    sede_id=int(sede_id) if sede_id else None,
                    consultorio_id=int(consultorio_id) if consultorio_id else None,
                    fecha=fecha,
                    hora=hora,
                    duracion_minutos=int(duracion),
                    notas=notas,
                    estado=EstadoTurno.CONFIRMADO,
                    creado_por=request.user,
                )
                turno.save()

                LogAuditoria.objects.create(
                    usuario=request.user,
                    accion="CREAR_TURNO",
                    entidad="Turno",
                    entidad_id=str(turno.id),
                    detalles=f"Turno creado: {turno.paciente.nombre_completo} con {turno.medico.nombre_completo} el {fecha} a las {hora_str}",
                    ip_origen=request.META.get('REMOTE_ADDR', '127.0.0.1')
                )

                messages.success(request, f'Turno creado para {turno.paciente.nombre_completo} el {fecha_str} a las {hora_str}')
                return redirect('recepcion_dashboard')
            except Exception as e:
                messages.error(request, f'Error al crear turno: {str(e)}')
        else:
            messages.error(request, 'Complete todos los campos obligatorios (Médico, Paciente, Fecha, Hora)')

    context = {
        'medicos': medicos,
        'pacientes': pacientes,
        'sedes': sedes,
        'consultorios': consultorios,
        'fecha_hoy': datetime.date.today().strftime('%Y-%m-%d'),
    }
    return render(request, 'recepcion/nuevo_turno.html', context)


@login_required
@role_required(['MEDICO', 'ADMIN', 'DEV'])
def medico_agenda(request):
    user_role = get_user_role(request.user)
    
    if user_role == 'MEDICO' and hasattr(request.user, 'perfil_medico'):
        medico = request.user.perfil_medico
    elif user_role in ['ADMIN', 'DEV']:
        # Admin/DEV pueden ver el primer medico demo
        medico = Medico.objects.filter(activo=True).first()
        if not medico:
            return redirect('recepcion_dashboard')
    else:
        return redirect('recepcion_dashboard')

    fecha_sel = datetime.date.today()
    turnos = Turno.objects.filter(medico=medico, fecha=fecha_sel).select_related('paciente', 'consultorio')
    
    context = {
        'medico': medico,
        'fecha_sel': fecha_sel,
        'turnos': turnos,
        'estados': EstadoTurno.choices,
    }
    return render(request, 'medicos/agenda.html', context)


@login_required
@role_required(['RECEPCION', 'MEDICO', 'ADMIN', 'DEV'])
def cambiar_estado_turno(request, turno_id):
    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        turno = get_object_or_404(Turno, id=turno_id)
        
        user_role = get_user_role(request.user)
        
        # Verificar que el medico solo pueda cambiar sus propios turnos
        if user_role == 'MEDICO':
            if turno.medico != request.user.perfil_medico:
                messages.error(request, 'No tiene permiso para modificar turnos de otros medicos')
                return redirect('medico_agenda')
        
        if nuevo_estado in dict(EstadoTurno.choices):
            turno.estado = nuevo_estado
            turno.save()
            
            # Auditoría
            LogAuditoria.objects.create(
                usuario=request.user,
                accion="CAMBIAR_ESTADO_TURNO",
                entidad="Turno",
                entidad_id=str(turno.id),
                detalles=f"Cambió estado a {nuevo_estado} para paciente {turno.paciente.nombre_completo}",
                ip_origen=request.META.get('REMOTE_ADDR', '127.0.0.1')
            )
            
    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or '/'
    return redirect(next_url)


@login_required
@role_required(['MEDICO', 'ADMIN', 'DEV'])
def paciente_historia_clinica(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    historias = HistoriaClinica.objects.filter(paciente=paciente).select_related('medico')
    
    # Registrar auditoría de acceso según Ley 26.529
    LogAuditoria.objects.create(
        usuario=request.user,
        accion="VER_HISTORIA_CLINICA",
        entidad="Paciente",
        entidad_id=str(paciente.id),
        detalles=f"Acceso a Historia Clínica de {paciente.nombre_completo} (DNI: {paciente.dni})",
        ip_origen=request.META.get('REMOTE_ADDR', '127.0.0.1')
    )

    user_role = get_user_role(request.user)
    
    if request.method == 'POST':
        # Solo medicos pueden crear evoluciones clinicas
        if user_role != 'MEDICO' and not hasattr(request.user, 'perfil_medico'):
            messages.error(request, 'Solo los medicos pueden crear registros clinicos')
            return redirect('paciente_historia_clinica', paciente_id=paciente.id)
        
        # Agregar evolución clínica
        motivo = request.POST.get('motivo_consulta')
        diagnostico = request.POST.get('diagnostico')
        notas = request.POST.get('notas_evolucion', '')
        tratamiento = request.POST.get('tratamiento_prescrito', '')
        
        medico = getattr(request.user, 'perfil_medico', None) or Medico.objects.filter(activo=True).first()
        
        hc = HistoriaClinica.objects.create(
            paciente=paciente,
            medico=medico,
            motivo_consulta=motivo,
            diagnostico=diagnostico,
            notas_evolucion=notas,
            tratamiento_prescrito=tratamiento
        )

        LogAuditoria.objects.create(
            usuario=request.user,
            accion="CREAR_HISTORIA_CLINICA",
            entidad="HistoriaClinica",
            entidad_id=str(hc.id),
            detalles=f"Creación de evolución médica para {paciente.nombre_completo}",
            ip_origen=request.META.get('REMOTE_ADDR', '127.0.0.1')
        )
        return redirect('paciente_historia_clinica', paciente_id=paciente.id)

    context = {
        'paciente': paciente,
        'historias': historias,
    }
    return render(request, 'pacientes/historia_clinica.html', context)


def turnero_pantalla(request):
    """Vista pública para Smart TV / Sala de Espera"""
    hoy = datetime.date.today()
    # Turnos del día en sala de espera o siendo llamados
    turnos_espera = Turno.objects.filter(
        fecha=hoy, 
        estado__in=[EstadoTurno.EN_ESPERA, EstadoTurno.CONFIRMADO]
    ).select_related('paciente', 'medico', 'consultorio')

    turnos_atendiendo = Turno.objects.filter(
        fecha=hoy,
        estado=EstadoTurno.ATENDIDO
    ).select_related('paciente', 'medico', 'consultorio').order_by('-id')[:3]

    config = ConfiguracionSistema.get_solo()

    context = {
        'config': config,
        'turnos_espera': turnos_espera,
        'turnos_atendiendo': turnos_atendiendo,
        'hora_actual': timezone.now(),
    }
    return render(request, 'turnero/pantalla.html', context)

