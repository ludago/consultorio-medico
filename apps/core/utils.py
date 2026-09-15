import logging

logger = logging.getLogger(__name__)


def safe_get_perfil(user):
    try:
        return getattr(user, 'perfil_usuario', None)
    except Exception as e:
        logger.warning('Error al obtener perfil_usuario para %s: %s', user, e)
        return None


def get_user_rol(user):
    perfil = safe_get_perfil(user)
    if perfil:
        return perfil.rol
    return None
