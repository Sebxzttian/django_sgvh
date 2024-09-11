from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Administrador, Instructor, ProgramaFormacion, Ambiente, Competencia
from django import forms

def is_admin(user):
    return user.is_authenticated and user.is_staff

# Formularios para cada modelo
class AdministradorForm(forms.ModelForm):
    class Meta:
        model = Administrador
        fields = ['nombres', 'apellidos', 'numero_cedula', 'numero_celular', 'correo_institucional', 'correo_personal']

class InstructorForm(forms.ModelForm):
    class Meta:
        model = Instructor
        fields = ['nombres', 'apellidos', 'correo_personal', 'correo_institucional', 'numero_celular', 'numero_cedula', 'competencias_imparte']

class ProgramaFormacionForm(forms.ModelForm):
    class Meta:
        model = ProgramaFormacion
        fields = ['nombre_programa', 'jornada', 'fecha_inicio', 'fecha_fin', 'instructores']

class AmbienteForm(forms.ModelForm):
    class Meta:
        model = Ambiente
        fields = ['nombre_ambiente', 'sede', 'programa_formacion', 'instructores']

class CompetenciaForm(forms.ModelForm):
    class Meta:
        model = Competencia
        fields = ['nombre', 'unidad_competencia', 'duracion_estimada', 'resultado_aprendizaje', 'instructor', 'programa_formacion']

# Vistas protegidas para cada entidad
class AdministradorListCreateView(LoginRequiredMixin, ListView):
    model = Administrador
    template_name = 'horarios/administrador_list.html'
    context_object_name = 'administradores'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AdministradorForm()
        return context
    
    def post(self, request, *args, **kwargs):
        form = AdministradorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('administrador_list')
        return self.get(request, *args, **kwargs)

class InstructorListCreateView(LoginRequiredMixin, ListView):
    model = Instructor
    template_name = 'horarios/instructor_list.html'
    context_object_name = 'instructores'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = InstructorForm()
        return context
    
    def post(self, request, *args, **kwargs):
        form = InstructorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('instructor_list')
        return self.get(request, *args, **kwargs)

class ProgramaFormacionListCreateView(LoginRequiredMixin, ListView):
    model = ProgramaFormacion
    template_name = 'horarios/programa_formacion_list.html'
    context_object_name = 'programas'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ProgramaFormacionForm()
        return context
    
    def post(self, request, *args, **kwargs):
        form = ProgramaFormacionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('programa_formacion_list')
        return self.get(request, *args, **kwargs)

class AmbienteListCreateView(LoginRequiredMixin, ListView):
    model = Ambiente
    template_name = 'horarios/ambiente_list.html'
    context_object_name = 'ambientes'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AmbienteForm()
        return context
    
    def post(self, request, *args, **kwargs):
        form = AmbienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ambiente_list')
        return self.get(request, *args, **kwargs)

class CompetenciaListCreateView(LoginRequiredMixin, ListView):
    model = Competencia
    template_name = 'horarios/competencia_list.html'
    context_object_name = 'competencias'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CompetenciaForm()
        return context
    
    def post(self, request, *args, **kwargs):
        form = CompetenciaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('competencia_list')
        return self.get(request, *args, **kwargs)

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

@login_required
def admin_dashboard(request):
    return render(request, 'horarios/admin_dashboard.html')
