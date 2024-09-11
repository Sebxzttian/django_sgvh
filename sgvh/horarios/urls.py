from django.urls import path
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required
from .views import (
    login_view, 
    admin_dashboard, 
    AdministradorListCreateView, 
    InstructorListCreateView, 
    ProgramaFormacionListCreateView, 
    AmbienteListCreateView, 
    CompetenciaListCreateView
)

urlpatterns = [
    # URLs públicas
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    # URLs protegidas
    path('dashboard/', login_required(admin_dashboard), name='admin_dashboard'),
    path('administradores/', login_required(AdministradorListCreateView.as_view()), name='administrador_list'),
    path('instructores/', login_required(InstructorListCreateView.as_view()), name='instructor_list'),
    path('programas/', login_required(ProgramaFormacionListCreateView.as_view()), name='programa_formacion_list'),
    path('ambientes/', login_required(AmbienteListCreateView.as_view()), name='ambiente_list'),
    path('competencias/', login_required(CompetenciaListCreateView.as_view()), name='competencia_list'),
]
