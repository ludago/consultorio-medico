from .decorators import get_user_role


def user_role_context(request):
    """Context processor que agrega el rol del usuario a todos los templates."""
    context = {
        'user_role': None,
        'is_recepcion': False,
        'is_medico': False,
        'is_admin': False,
        'is_dev': False,
    }
    
    if request.user.is_authenticated:
        role = get_user_role(request.user)
        context['user_role'] = role
        context['is_recepcion'] = role == 'RECEPCION'
        context['is_medico'] = role == 'MEDICO'
        context['is_admin'] = role in ['ADMIN', 'DEV']
        context['is_dev'] = role == 'DEV'
    
    return context
