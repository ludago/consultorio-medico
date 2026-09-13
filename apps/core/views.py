import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.utils import timezone
from django.db.models import Q

from apps.configuracion.models import ConfiguracionSistema
from apps.usuarios.models import Medico, Especialidad, Sede
from apps.pacientes.models import Paciente
from apps.turnos.models import Turno, EstadoTurno
from apps.historias_clinicas.models import HistoriaClinica
from apps.auditoria.models import LogAuditoria

def home_redirect(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')
    
    # Redirigir a vista médico si es médico, o a recepción
    if hasattr(request.user, 'perfil_medico'):
        return redirect('medico_agenda')
    return redirect('recepcion_dashboard')

@login_required
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
def medico_agenda(request):
    if not hasattr(request.user, 'perfil_medico'):
        # Si no es médico pero es staff, permitir ver la agenda del primer médico demo
        medico = Medico.objects.filter(activo=True).first()
        if not medico:
            return redirect('recepcion_dashboard')
    else:
        medico = request.user.perfil_medico

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
def cambiar_estado_turno(request, turno_id):
    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        turno = get_object_or_404(Turno, id=turno_id)
        
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

    if request.method == 'POST':
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
