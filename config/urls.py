from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from apps.core import views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Autenticación
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='/accounts/login/'), name='logout'),

    # Rutas Principales
    path('', core_views.home_redirect, name='home'),
    path('recepcion/', core_views.recepcion_dashboard, name='recepcion_dashboard'),
    path('recepcion/nuevo-turno/', core_views.nuevo_turno, name='nuevo_turno'),
    path('medico/agenda/', core_views.medico_agenda, name='medico_agenda'),
    path('turnos/<int:turno_id>/cambiar-estado/', core_views.cambiar_estado_turno, name='cambiar_estado_turno'),
    path('pacientes/<int:paciente_id>/historia-clinica/', core_views.paciente_historia_clinica, name='paciente_historia_clinica'),
    path('turnero/', core_views.turnero_pantalla, name='turnero_pantalla'),
]
