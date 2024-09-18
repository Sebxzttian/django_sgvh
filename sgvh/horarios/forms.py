from django import forms
from .models import Administrador, Instructor, ProgramaFormacion, Ambiente, Competencia

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
        fields = ['nombre', 'codigo_norma', 'unidad_competencia', 'duracion_estimada', 'resultado_aprendizaje', 'instructor', 'programa_formacion']
