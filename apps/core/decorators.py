import logging
from functools import wraps
from django.shortcuts import redirect, render
from django.contrib import messages
from .utils import safe_get_perfil

logger = logging.getLogger(__name__)


def role_required(roles_permitidos, redirect_url=None):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('/accounts/login/')

            perfil = safe_get_perfil(request.user)
            if not perfil:
                messages.error(request, 'No tiene un perfil de usuario asignado.')
                return redirect('/')

            if perfil.rol not in roles_permitidos:
                messages.error(
                    request,
                    'No tiene permisos para acceder a esta seccion. '
                    'Se requiere uno de estos roles: ' + ', '.join(roles_permitidos)
                )
                if redirect_url:
                    return redirect(redirect_url)
                return render(request, '403.html', status=403)

            request.user_role = perfil.rol
            return view_func(request, *args, **kwargs)

        return _wrapped_view
    return decorator


def get_user_role(user):
    perfil = safe_get_perfil(user)
    if perfil:
        return perfil.rol
    return None


def has_role(user, role):
    user_role = get_user_role(user)
    return user_role == role


def is_in_role(user, roles):
    user_role = get_user_role(user)
    return user_role in roles
