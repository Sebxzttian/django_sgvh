from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required
from . import views
from .views import (
    login_view, 
    admin_dashboard, 
    AdministradorListView,
    AdministradorCreateView,
    AdministradorUpdateView,
    AdministradorDeleteView,
    InstructorListView,
    InstructorCreateView,
    InstructorUpdateView,
    InstructorDeleteView,
    ProgramaFormacionListView,
    ProgramaFormacionCreateView,
    ProgramaFormacionUpdateView,
    ProgramaFormacionDeleteView,
    AmbienteListView,
    AmbienteCreateView,
    AmbienteUpdateView,
    AmbienteDeleteView,
    CompetenciaListView,
    CompetenciaCreateView,
    CompetenciaUpdateView,
    CompetenciaDeleteView,
    CalInstListView,
    CalInstCreateView,
    CalInstUpdateView,
    CalInstDeleteView,
    CalAmbListView,
    CalAmbCreateView,
    CalAmbUpdateView,
    CalAmbDeleteView,
    CalPFListView,
    CalPFCreateView,
    CalPFUpdateView,
    CalPFDeleteView,
    CalendarListView,
    CalendarCreateView,
    CalendarUpdateView,
    CalendarDeleteView,
    get_all_events,
    upload_instructors_csv
)

urlpatterns = [
    # Autenticación
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    # Cambio de contraseña
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='horarios/password_change.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='horarios/password_change_done.html'), name='password_change_done'),

    # Dashboard protegido
    path('dashboard/', login_required(admin_dashboard), name='admin_dashboard'),

    # Administradores
    path('administradores/', login_required(AdministradorListView.as_view()), name='administrador_list'),
    path('administradores/create/', login_required(AdministradorCreateView.as_view()), name='administrador_create'),
    path('administradores/<int:pk>/edit/', login_required(AdministradorUpdateView.as_view()), name='administrador_edit'),
    path('administradores/<int:pk>/delete/', login_required(AdministradorDeleteView.as_view()), name='administrador_delete'),

    # Instructores
    path('instructores/', login_required(InstructorListView.as_view()), name='instructor_list'),
    path('instructores/create/', login_required(InstructorCreateView.as_view()), name='instructor_create'),
    path('instructores/<int:pk>/edit/', login_required(InstructorUpdateView.as_view()), name='instructor_edit'),
    path('instructores/<int:pk>/delete/', login_required(InstructorDeleteView.as_view()), name='instructor_delete'),

    # Programas de formación
    path('programas/', login_required(ProgramaFormacionListView.as_view()), name='programa_formacion_list'),
    path('programas/create/', login_required(ProgramaFormacionCreateView.as_view()), name='programa_formacion_create'),
    path('programas/<int:pk>/edit/', login_required(ProgramaFormacionUpdateView.as_view()), name='programa_formacion_edit'),
    path('programas/<int:pk>/delete/', login_required(ProgramaFormacionDeleteView.as_view()), name='programa_formacion_delete'),

    # Ambientes
    path('ambientes/', login_required(AmbienteListView.as_view()), name='ambiente_list'),
    path('ambientes/create/', login_required(AmbienteCreateView.as_view()), name='ambiente_create'),
    path('ambientes/<int:pk>/edit/', login_required(AmbienteUpdateView.as_view()), name='ambiente_edit'),
    path('ambientes/<int:pk>/delete/', login_required(AmbienteDeleteView.as_view()), name='ambiente_delete'),

    # Competencias
    path('competencias/', login_required(CompetenciaListView.as_view()), name='competencia_list'),
    path('competencias/create/', login_required(CompetenciaCreateView.as_view()), name='competencia_create'),
    path('competencias/<int:pk>/edit/', login_required(CompetenciaUpdateView.as_view()), name='competencia_edit'),
    path('competencias/<int:pk>/delete/', login_required(CompetenciaDeleteView.as_view()), name='competencia_delete'),

    # Calendario de Instructores
    path('calinsts/', login_required(CalInstListView.as_view()), name='calinst_list'),
    path('calinsts/create/', login_required(CalInstCreateView.as_view()), name='calinst_create'),
    path('calinsts/<int:pk>/edit/', login_required(CalInstUpdateView.as_view()), name='calinst_edit'),
    path('calinsts/<int:pk>/delete/', login_required(CalInstDeleteView.as_view()), name='calinst_delete'),

    # Calendario de Ambiente
    path('calambs/', login_required(CalAmbListView.as_view()), name='calamb_list'),
    path('calambs/create/', login_required(CalAmbCreateView.as_view()), name='calamb_create'),
    path('calambs/<int:pk>/edit/', login_required(CalAmbUpdateView.as_view()), name='calamb_edit'),
    path('calambs/<int:pk>/delete/', login_required(CalAmbDeleteView.as_view()), name='calamb_delete'),

    # Calendario de Programa de formacion
    path('calpfs/', login_required(CalPFListView.as_view()), name='calpf_list'),
    path('calpfs/create/', login_required(CalPFCreateView.as_view()), name='calpf_create'),
    path('calpfs/<int:pk>/edit/', login_required(CalPFUpdateView.as_view()), name='calpf_edit'),
    path('calpfs/<int:pk>/delete/', login_required(CalPFDeleteView.as_view()), name='calpf_delete'),

        # Calendarios
    path('calendars/', login_required(CalendarListView.as_view()), name='calendar_list'),
    path('calendars/create/', login_required(CalendarCreateView.as_view()), name='calendar_create'),
    path('calendars/<int:pk>/edit/', login_required(CalendarUpdateView.as_view()), name='calendar_edit'),
    path('calendars/<int:pk>/delete/', login_required(CalendarDeleteView.as_view()), name='calendar_delete'),

    # Obtener todos los eventos
    path('eventos/', get_all_events, name='get_all_events'),

    # cargar instructores por medio de un archivo
    path('instructores/upload/', upload_instructors_csv, name='upload_instructors_csv'),  # Ase
]
