from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from .models import Administrador, Instructor, ProgramaFormacion, Ambiente, Competencia

def is_admin(user):
    return user.is_authenticated and user.is_staff

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return is_admin(self.request.user)

class AdministradorListView(AdminRequiredMixin, ListView):
    model = Administrador
    template_name = 'administrador_list.html'
    context_object_name = 'administradores'

class AdministradorCreateView(AdminRequiredMixin, CreateView):
    model = Administrador
    fields = ['nombres', 'apellidos', 'numero_cedula', 'numero_celular', 'correo_institucional', 'correo_personal']
    template_name = 'administrador_form.html'
    success_url = reverse_lazy('administrador_list')

class InstructorListView(AdminRequiredMixin, ListView):
    model = Instructor
    template_name = 'horarios/instructor_list.html'
    context_object_name = 'instructores'

class InstructorCreateView(AdminRequiredMixin, CreateView):
    model = Instructor
    fields = ['nombres', 'apellidos', 'correo_personal', 'correo_institucional', 'numero_celular', 'numero_cedula', 'competencias_imparte']
    template_name = 'horarios/instructor_form.html'
    success_url = reverse_lazy('instructor_list')

class ProgramaFormacionListView(AdminRequiredMixin, ListView):
    model = ProgramaFormacion
    template_name = 'horarios/programa_formacion_list.html'
    context_object_name = 'programas'

class ProgramaFormacionCreateView(AdminRequiredMixin, CreateView):
    model = ProgramaFormacion
    fields = ['nombre_programa', 'jornada', 'fecha_inicio', 'fecha_fin', 'instructores']
    template_name = 'horarios/programa_formacion_form.html'
    success_url = reverse_lazy('programa_formacion_list')

class AmbienteListView(AdminRequiredMixin, ListView):
    model = Ambiente
    template_name = 'horarios/ambiente_list.html'
    context_object_name = 'ambientes'

class AmbienteCreateView(AdminRequiredMixin, CreateView):
    model = Ambiente
    fields = ['nombre_ambiente', 'sede', 'programa_formacion', 'instructores']
    template_name = 'horarios/ambiente_form.html'
    success_url = reverse_lazy('ambiente_list')

class CompetenciaListView(AdminRequiredMixin, ListView):
    model = Competencia
    template_name = 'horarios/competencia_list.html'
    context_object_name = 'competencias'

class CompetenciaCreateView(AdminRequiredMixin, CreateView):
    model = Competencia
    fields = ['nombre', 'unidad_competencia', 'duracion_estimada', 'resultado_aprendizaje', 'instructor', 'programa_formacion']
    template_name = 'horarios/competencia_form.html'
    success_url = reverse_lazy('competencia_list')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            error_message = "Credenciales inválidas o usuario no es administrador."
            return render(request, 'horarios/login.html', {'error_message': error_message})
    return render(request, 'horarios/login.html')

@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(request, 'horarios/admin_dashboard.html')