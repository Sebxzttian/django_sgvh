from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Administrador, Instructor, ProgramaFormacion, Ambiente, Competencia
from calendarios.models import CalInst, CalAmb, CalPF

class AdministradorForm(UserCreationForm):
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text="La contraseña debe tener al menos 8 caracteres."
    )
    password2 = forms.CharField(
        label="Confirmar Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text="Repita la contraseña para verificar."
    )

    class Meta:
        model = Administrador
        fields = ['nombres', 'apellidos', 'numero_cedula', 'numero_celular', 'correo_institucional', 'password1', 'password2']
        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_cedula': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_celular': forms.TextInput(attrs={'class': 'form-control'}),
            'correo_institucional': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class InstructorForm(forms.ModelForm):
    class Meta:
        model = Instructor
        fields = ['nombres', 'apellidos', 'correo_institucional', 'numero_celular', 'numero_cedula', 'competencias_imparte']
        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
            'correo_institucional': forms.EmailInput(attrs={'class': 'form-control'}),
            'numero_celular': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_cedula': forms.TextInput(attrs={'class': 'form-control'}),
            'competencias_imparte': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ProgramaFormacionForm(forms.ModelForm):
    class Meta:
        model = ProgramaFormacion
        fields = ['codigo_programa', 'nombre_programa', 'jornada', 'fecha_inicio', 'fecha_fin']
        widgets = {
            'codigo_programa': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_programa': forms.TextInput(attrs={'class': 'form-control'}),
            'jornada': forms.Select(attrs={'class': 'form-control'}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class AmbienteForm(forms.ModelForm):
    class Meta:
        model = Ambiente
        fields = ['codigo_ambiente', 'nombre_ambiente', 'sede']
        widgets = {
            'nombre_ambiente': forms.TextInput(attrs={'class': 'form-control'}),
            'sede': forms.Select(attrs={'class': 'form-control'}),
        }

class CompetenciaForm(forms.ModelForm):
    class Meta:
        model = Competencia
        fields = ['nombre', 'codigo_norma', 'unidad_competencia', 'duracion_estimada', 'resultado_aprendizaje']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'norma': forms.TextInput(attrs={'class': 'form-control'}),
            'unidad_competencia': forms.TextInput(attrs={'class': 'form-control'}),
            'duracion_estimada': forms.TextInput(attrs={'class': 'form-control'}),
            'resultado_aprendizaje': forms.Textarea(attrs={'class': 'form-control'}),
        }

class CalInstForm(forms.ModelForm):
    class Meta:
        model = CalInst
        fields = ['programa', 'ambiente', 'competencia', 'start', 'end']
        widgets = {
            'programa': forms.Select(attrs={'class': 'form-control'}),
            'ambiente': forms.Select(attrs={'class': 'form-control'}),
            'competencia': forms.Select(attrs={'class': 'form-control'}),
            'start': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'end': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }

class CalAmbForm(forms.ModelForm):
    class Meta:
        model = CalAmb
        fields = ['instructor', 'programa', 'competencia', 'start', 'end']
        widgets = {
            'instructor': forms.Select(attrs={'class': 'form-control'}),
            'programa': forms.Select(attrs={'class': 'form-control'}),
            'competencia': forms.Select(attrs={'class': 'form-control'}),
            'start': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'end': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }