from functools import wraps
from django.shortcuts import redirect, render
from django.contrib import messages


def role_required(roles_permitidos, redirect_url=None):
    """
    Decorador que verifica si el usuario tiene uno de los roles permitidos.
    
    Uso:
        @role_required(['RECEPCION', 'ADMIN', 'DEV'])
        def mi_vista(request):
            ...
    
    Si el usuario no tiene el rol requerido, redirige a 403 o al redirect_url.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('/accounts/login/')
            
            # Verificar si tiene perfil de usuario
            perfil = getattr(request.user, 'perfil_usuario', None)
            if not perfil:
                messages.error(request, 'No tiene un perfil de usuario asignado.')
                return redirect('/')
            
            # Verificar si el rol esta en los permitidos
            if perfil.rol not in roles_permitidos:
                messages.error(
                    request, 
                    f'No tiene permisos para acceder a esta seccion. '
                    f'Se requiere uno de estos roles: {", ".join(roles_permitidos)}'
                )
                if redirect_url:
                    return redirect(redirect_url)
                return render(request, '403.html', status=403)
            
            # Agregar el rol al request para uso en templates
            request.user_role = perfil.rol
            return view_func(request, *args, **kwargs)
        
        return _wrapped_view
    return decorator


def get_user_role(user):
    """Obtiene el rol del usuario desde su perfil."""
    perfil = getattr(user, 'perfil_usuario', None)
    if perfil:
        return perfil.rol
    return None


def has_role(user, role):
    """Verifica si el usuario tiene un rol especifico."""
    user_role = get_user_role(user)
    return user_role == role


def is_in_role(user, roles):
    """Verifica si el usuario tiene alguno de los roles especificados."""
    user_role = get_user_role(user)
    return user_role in roles

