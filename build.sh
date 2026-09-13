#!/usr/bin/env bash
set -o errexit

echo "=== Instalando dependencias ==="
pip install -r requirements.txt

echo "=== Recopilando archivos estaticos ==="
python manage.py collectstatic --no-input

echo "=== Aplicando migraciones ==="
python manage.py migrate

echo "=== Cargando datos demo ==="
python manage.py seed_demo 2>/dev/null || echo "Datos demo ya cargados o error"

echo "=== Creando superuser por defecto ==="
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
    print('Superuser admin creado')
else:
    print('Superuser admin ya existe')
"

echo "=== Build completado ==="
