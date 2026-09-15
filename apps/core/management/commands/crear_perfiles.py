from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.usuarios.models import PerfilUsuario

class Command(BaseCommand):
    help = 'Crea perfiles de usuario con roles para usuarios existentes.'

    def handle(self, *args, **options):
        # Mapeo de usuarios a roles
        roles_map = {
            'desarrollador': 'DEV',
            'admin': 'ADMIN',
            'recepcion': 'RECEPCION',
            'dr.garcia': 'MEDICO',
            'dra.martinez': 'MEDICO',
        }

        for username, rol in roles_map.items():
            try:
                user = User.objects.get(username=username)
                perfil, created = PerfilUsuario.objects.get_or_create(
                    user=user,
                    defaults={'rol': rol}
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"[OK] Perfil creado para {username}: {rol}"))
                else:
                    self.stdout.write(self.style.WARNING(f"[SKIP] Perfil ya existe para {username}: {perfil.rol}"))
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"[ERROR] Usuario {username} no existe"))
