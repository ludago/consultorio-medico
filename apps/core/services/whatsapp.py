import logging
from django.conf import settings
from apps.configuracion.models import ConfiguracionSistema

logger = logging.getLogger(__name__)

def enviar_mensaje_whatsapp(numero_destino, mensaje):
    """
    Servicio unificado de envío de WhatsApp vía Twilio API.
    Si las credenciales de Twilio están configuradas, envía el mensaje real.
    De lo contrario, en modo Demo/Desarrollo, registra el log para auditoría.
    """
    config = ConfiguracionSistema.get_solo()
    
    # Formatear número argentino si es necesario
    if not numero_destino.startswith('+'):
        numero_destino = f"+549{numero_destino}"

    account_sid = getattr(settings, 'TWILIO_ACCOUNT_SID', None)
    auth_token = getattr(settings, 'TWILIO_AUTH_TOKEN', None)
    from_whatsapp = getattr(settings, 'TWILIO_WHATSAPP_NUMBER', 'whatsapp:+14155238886')

    if account_sid and auth_token:
        try:
            from twilio.rest import Client
            client = Client(account_sid, auth_token)
            message = client.messages.create(
                body=mensaje,
                from_=from_whatsapp,
                to=f"whatsapp:{numero_destino}"
            )
            logger.info(f"WhatsApp enviado exitosamente a {numero_destino} (SID: {message.sid})")
            return True, message.sid
        except Exception as e:
            logger.error(f"Error enviando WhatsApp via Twilio a {numero_destino}: {str(e)}")
            return False, str(e)
    else:
        # Modo Simulación / Demo en desarrollo
        print(f"\n[SIMULACIÓN WHATSAPP] Para: {numero_destino}\nMensaje:\n{mensaje}\n-----------------------------------")
        return True, "SIMULADO_DEMO"
