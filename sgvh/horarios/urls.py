from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    AdministradorListView, AdministradorCreateView,
    InstructorListView, InstructorCreateView,
    ProgramaFormacionListView, ProgramaFormacionCreateView,
    AmbienteListView, AmbienteCreateView,
    CompetenciaListView, CompetenciaCreateView,
    login_view, admin_dashboard
)

urlpatterns = [
    # URL pública para inicio de sesión
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    # URLs protegidas
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('administradores/', AdministradorListView.as_view(), name='administrador_list'),
    path('administradores/crear/', AdministradorCreateView.as_view(), name='administrador_create'),
    path('instructores/', InstructorListView.as_view(), name='instructor_list'),
    path('instructores/crear/', InstructorCreateView.as_view(), name='instructor_create'),
    path('programas/', ProgramaFormacionListView.as_view(), name='programa_formacion_list'),
    path('programas/crear/', ProgramaFormacionCreateView.as_view(), name='programa_formacion_create'),
    path('ambientes/', AmbienteListView.as_view(), name='ambiente_list'),
    path('ambientes/crear/', AmbienteCreateView.as_view(), name='ambiente_create'),
    path('competencias/', CompetenciaListView.as_view(), name='competencia_list'),
    path('competencias/crear/', CompetenciaCreateView.as_view(), name='competencia_create'),
]