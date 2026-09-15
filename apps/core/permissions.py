from django.contrib.auth.decorators import login_required
from .decorators import role_required, get_user_role, has_role, is_in_role


def recepcion_required(view_func):
    """Decorador: solo recepcion, admin o dev."""
    return role_required(['RECEPCION', 'ADMIN', 'DEV'])(view_func)


def medico_required(view_func):
    """Decorador: solo medico, admin o dev."""
    return role_required(['MEDICO', 'ADMIN', 'DEV'])(view_func)


def admin_required(view_func):
    """Decorador: solo admin o dev."""
    return role_required(['ADMIN', 'DEV'])(view_func)


def dev_required(view_func):
    """Decorador: solo dev."""
    return role_required(['DEV'])(view_func)


def login_and_role_required(roles_permitidos):
    """Combinacion de login_required + role_required."""
    def decorator(view_func):
        return login_required(
            role_required(roles_permitidos)(view_func)
        )
    return decorator
