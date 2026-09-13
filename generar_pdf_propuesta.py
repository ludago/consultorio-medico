import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def generar_pdf():
    pdf_filename = "Propuesta_y_Guia_Demo_Consultorio_Medico.pdf"
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        rightMargin=0.5 * inch,
        leftMargin=0.5 * inch,
        topMargin=0.5 * inch,
        bottomMargin=0.5 * inch
    )

    styles = getSampleStyleSheet()

    # Estilos Personalizados de Alto Nivel
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=colors.HexColor('#0f172a'),
        alignment=0, # Izquierda
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#0284c7'),
        spaceAfter=15
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor('#0f172a'),
        spaceBefore=14,
        spaceAfter=8
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#334155'),
        spaceAfter=8
    )

    bullet_style = ParagraphStyle(
        'BulletDark',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )

    badge_green = ParagraphStyle(
        'BadgeGreen',
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#15803d')
    )

    badge_yellow = ParagraphStyle(
        'BadgeYellow',
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#b45309')
    )

    story = []

    # Header / Banner Principal
    story.append(Paragraph("SISTEMA DE GESTIÓN DE CONSULTORIO MÉDICO", title_style))
    story.append(Paragraph("Propuesta Técnica Comercial & Guía Interactiva de Demostración", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#0284c7'), spaceAfter=15))

    # Resumen Ejecutivo
    story.append(Paragraph("<b>1. Resumen Ejecutivo & Visión del Producto</b>", h2_style))
    story.append(Paragraph(
        "Plataforma profesional de gestión médica de alta gama orientada a consultorios en Argentina. "
        "Ofrece una experiencia fluida, rápida y segura en el día a día para médicos y recepcionistas, "
        "con cumplimiento legal completo (Ley 25.326 de Protección de Datos Personales y Ley 26.529 de Historia Clínica).",
        body_style
    ))

    # Tabla de Estado de Funcionalidades
    story.append(Paragraph("<b>2. Funcionalidades del Sistema — Estado Actual vs. Próximas Fases</b>", h2_style))
    
    tabla_data = [
        [Paragraph("<b>Funcionalidad</b>", body_style), Paragraph("<b>Descripción y Alcance</b>", body_style), Paragraph("<b>Estado</b>", body_style)],
        
        [Paragraph("<b>Agenda Mobile Médico</b>", body_style), Paragraph("Vista mobile-first para smartphones. Visualización de turnos del día, estados e historia clínica a 1 toque.", body_style), Paragraph("🟢 <b>CONSTRUIDO Y ACTIVO</b>", badge_green)],
        [Paragraph("<b>Panel de Recepción</b>", body_style), Paragraph("Dashboard multi-médico con filtros por fecha/especialidad, estadísticas del día y cambio rápido de estados.", body_style), Paragraph("🟢 <b>CONSTRUIDO Y ACTIVO</b>", badge_green)],
        [Paragraph("<b>Turnero TV Sala Espera</b>", body_style), Paragraph("Pantalla pública para Smart TV. Reloj en vivo, pacientes aguardando y llamadas destacadas al consultorio.", body_style), Paragraph("🟢 <b>CONSTRUIDO Y ACTIVO</b>", badge_green)],
        [Paragraph("<b>Historia Clínica Legal</b>", body_style), Paragraph("Evoluciones clínicas con borrado lógico (Soft-Delete obligatorio de 10 años conforme a Ley 26.529).", body_style), Paragraph("🟢 <b>CONSTRUIDO Y ACTIVO</b>", badge_green)],
        [Paragraph("<b>Regla de Licencia / Cupos</b>", body_style), Paragraph("Restricción de seguridad para cupo de médicos (actualmente en 2 médicos demo, ampliable a 10 o ilimitado).", body_style), Paragraph("🟢 <b>CONSTRUIDO Y ACTIVO</b>", badge_green)],
        [Paragraph("<b>Seguridad & Auditoría</b>", body_style), Paragraph("Registro trazable de accesos (LogAuditoria) y almacenamiento de consentimiento del paciente (Ley 25.326).", body_style), Paragraph("🟢 <b>CONSTRUIDO Y ACTIVO</b>", badge_green)],
        [Paragraph("<b>WhatsApp Notificaciones</b>", body_style), Paragraph("Integración con Twilio API lista para activar notificaciones automáticas al médico y paciente.", body_style), Paragraph("🟢 <b>CÓDIGO LISTO / DEMO</b>", badge_green)],
        
        [Paragraph("<b>Facturación AFIP</b>", body_style), Paragraph("Emisión de comprobantes A/B/C integrados (Fase posterior a validar con contador/clínica).", body_style), Paragraph("🟡 <b>PREPARADO EN MODELO</b>", badge_yellow)],
        [Paragraph("<b>Obras Sociales & Prepagas</b>", body_style), Paragraph("Validación de afiliados y nomencladores nacionales (Fase posterior a confirmar con obras sociales).", body_style), Paragraph("🟡 <b>PREPARADO EN MODELO</b>", badge_yellow)],
        [Paragraph("<b>Receta Electrónica PDF</b>", body_style), Paragraph("Módulo de generación de recetas con formato específico (Fase posterior según especialidad).", body_style), Paragraph("🟡 <b>PREPARADO EN MODELO</b>", badge_yellow)],
    ]

    t = Table(tabla_data, colWidths=[1.8*inch, 3.8*inch, 1.8*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f5f9')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#0f172a')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 15))

    # Guía Paso a Paso para la Prueba del Médico y Secretaria
    story.append(Paragraph("<b>3. Guía de Prueba Interactiva Paso a Paso (Para el Médico y Secretaria)</b>", h2_style))
    story.append(Paragraph("El médico y su secretaria pueden ingresar directamente a la Demo sin necesidad de instalar nada:", body_style))

    story.append(Paragraph("<b>Paso 1: Acceso de la Secretaria (Recepción)</b>", body_style))
    story.append(Paragraph("• Abrir en la computadora del mostrador o tablet la URL de Recepción.", bullet_style))
    story.append(Paragraph("• Ingresar con Usuario: <b>recepcion</b> | Clave: <b>recepcion123</b>", bullet_style))
    story.append(Paragraph("• Probar filtrar por el <b>Dr. Alejandro García</b> o la <b>Dra. Sofía Martínez</b>.", bullet_style))
    story.append(Paragraph("• Tocar el botón amarillo <b>'Anunciar Llegada'</b> en un paciente para pasarlo a Sala de Espera.", bullet_style))

    story.append(Paragraph("<b>Paso 2: Acceso del Médico desde su Celular</b>", body_style))
    story.append(Paragraph("• Abrir en el teléfono inteligente (iPhone/Android) del médico la URL de la Agenda.", bullet_style))
    story.append(Paragraph("• Ingresar con Usuario: <b>dr.garcia</b> | Clave: <b>medico123</b>", bullet_style))
    story.append(Paragraph("• Observar los turnos agendados en tiempo real con sus horarios y datos del paciente.", bullet_style))
    story.append(Paragraph("• Tocar el botón verde <b>'Iniciar / Atendido'</b> en 1 solo toque.", bullet_style))
    story.append(Paragraph("• Ingresar al botón <b>'Historia Clínica'</b> para redactar una evolución y presionar guardar.", bullet_style))

    story.append(Paragraph("<b>Paso 3: Pantalla de Sala de Espera (Smart TV)</b>", body_style))
    story.append(Paragraph("• Abrir la URL del Turnero en la pantalla o Smart TV de la clínica.", bullet_style))
    story.append(Paragraph("• Observar el reloj digital en vivo y la llamada destacada en verde al paciente atendido.", bullet_style))

    story.append(Spacer(1, 15))

    # Guía para enviar la Demo Interactiva sin videollamada
    story.append(Paragraph("<b>4. ¿Cómo enviar la Demo Interactiva al Médico para que la pruebe en vivo?</b>", h2_style))
    story.append(Paragraph(
        "Para que el médico y su secretaria puedan probar el sistema <b>directamente desde sus propios celulares y computadoras</b> "
        "(sin necesidad de hacer videollamada), disponemos de 2 alternativas de acceso instantáneo:",
        body_style
    ))

    story.append(Paragraph("<b>Opción A (Recomendada - Enlace Público Instantáneo por WhatsApp):</b>", body_style))
    story.append(Paragraph("Se genera un enlace seguro de demostración en vivo (ejemplo: <code>https://consultorio-demo.loca.lt</code> o via Ngrok/Tunnel). Le envías ese enlace por WhatsApp al médico y a su secretaria junto con este PDF. Ellos abren el link en sus celulares y pueden interactuar simultáneamente en tiempo real.", body_style))

    story.append(Paragraph("<b>Opción B (Servidor Staging 24/7 en la Nube):</b>", body_style))
    story.append(Paragraph("Subimos la aplicación a un servidor de prueba 24 horas (como Render o Railway) con su propio dominio web. El enlace permanece activo todo el tiempo para que el médico lo revise cuando tenga un espacio libre entre consultas.", body_style))

    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#cbd5e1'), spaceAfter=10))
    story.append(Paragraph("<i>Documento generado automáticamente para presentación técnico-comercial. Consultorio Médico San Lucas.</i>", ParagraphStyle('Foot', parent=body_style, fontSize=8, textColor=colors.HexColor('#64748b'), alignment=1)))

    doc.build(story)
    print(f"[OK] PDF Generado exitosamente: {pdf_filename}")

if __name__ == '__main__':
    generar_pdf()
