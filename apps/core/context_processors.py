from .utils import get_user_rol


def user_role_context(request):
    context = {
        'user_role': None,
        'is_recepcion': False,
        'is_medico': False,
        'is_admin': False,
        'is_dev': False,
    }

    try:
        if request.user.is_authenticated:
            role = get_user_rol(request.user)
            context['user_role'] = role
            context['is_recepcion'] = role == 'RECEPCION'
            context['is_medico'] = role == 'MEDICO'
            context['is_admin'] = role in ['ADMIN', 'DEV']
            context['is_dev'] = role == 'DEV'
    except Exception:
        pass

    return context
