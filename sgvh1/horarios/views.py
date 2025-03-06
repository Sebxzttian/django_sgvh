from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from .models import Administrador, Instructor, ProgramaFormacion, Ambiente, Competencia
from calendarios.models import Calendar
from .forms import AdministradorForm, InstructorForm, ProgramaFormacionForm, AmbienteForm, CompetenciaForm, CalInstForm, CalAmbForm, CalPFForm, CalendarForm
from datetime import date
from django.http import JsonResponse, FileResponse  # Importar JsonResponse y FileResponse
import pandas as pd
from django.contrib import messages
from django.core.exceptions import ValidationError
from .utils import create_instructor_template
import os
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.db.models import Q


# Vistas para gestionar el cambio de contraseña con "Volver"
def set_password_change_return(request):
    """
    Guarda la URL actual en la sesión y redirige a la vista de cambio de contraseña.
    Permite que el botón "Volver" regrese a la página desde donde se solicitó el cambio.
    """
    # Guardar la URL de referencia o la URL actual en la sesión
    referer = request.META.get('HTTP_REFERER')
    
    # Si no hay referencia, usar el dashboard como valor predeterminado
    if not referer:
        request.session['password_change_return_url'] = reverse('admin_dashboard')
    else:
        request.session['password_change_return_url'] = referer
    
    return redirect('password_change')


class CustomPasswordChangeView(PasswordChangeView):
    """
    Vista personalizada para cambio de contraseña que incluye la URL de retorno
    para el botón "Volver".
    """
    template_name = 'horarios/password_change.html'  
    success_url = reverse_lazy('password_change_done')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtener la URL guardada, o usar una URL predeterminada
        return_url = self.request.session.get('password_change_return_url')
        if not return_url:
            return_url = reverse('admin_dashboard')
        context['return_url'] = return_url
        return context


# Vistas para Administrador
class AdministradorListView(LoginRequiredMixin, ListView):
    model = Administrador
    template_name = 'horarios/administradores/administrador_list.html'
    context_object_name = 'administradores'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AdministradorForm()
        return context

class AdministradorCreateView(LoginRequiredMixin, CreateView):
    model = Administrador
    form_class = AdministradorForm
    template_name = 'horarios/administradores/administrador_form.html'
    success_url = reverse_lazy('administrador_list')


class AdministradorUpdateView(LoginRequiredMixin, UpdateView):
    model = Administrador
    form_class = AdministradorForm
    template_name = 'horarios/administradores/administrador_form.html'
    success_url = reverse_lazy('administrador_list')


class AdministradorDeleteView(LoginRequiredMixin, DeleteView):
    model = Administrador
    template_name = 'horarios/administradores/administrador_confirm_delete.html'
    success_url = reverse_lazy('administrador_list')


# Vistas para Instructor
class InstructorListView(LoginRequiredMixin, ListView):
    model = Instructor
    template_name = 'horarios/instructores/instructor_list.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        queryset = Instructor.objects.all()
        search_query = self.request.GET.get('search', '').strip()

        if search_query:
            queryset = queryset.filter(
                Q(nombres__icontains=search_query) |
                Q(apellidos__icontains=search_query) |
                Q(correo_institucional__icontains=search_query) |
                Q(numero_celular__icontains=search_query) |
                Q(numero_cedula__icontains=search_query)
            ).distinct()

        return queryset.order_by('nombres', 'apellidos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        return context

class InstructorCreateView(LoginRequiredMixin, CreateView):
    model = Instructor
    form_class = InstructorForm
    template_name = 'horarios/instructores/instructor_form.html'
    success_url = reverse_lazy('instructor_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        instructor = self.object
        messages.success(self.request, f'¡Éxito! El instructor {instructor.nombres} {instructor.apellidos} ha sido creado correctamente.')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Error al crear el instructor. Por favor, verifica los datos.')
        return super().form_invalid(form)

class InstructorUpdateView(LoginRequiredMixin, UpdateView):
    model = Instructor
    form_class = InstructorForm
    template_name = 'horarios/instructores/instructor_form.html'
    success_url = reverse_lazy('instructor_list')

class InstructorDeleteView(LoginRequiredMixin, DeleteView):
    model = Instructor
    success_url = reverse_lazy('instructor_list')
    
    def delete(self, request, *args, **kwargs):
        try:
            instructor = self.get_object()
            nombre_completo = f"{instructor.nombres} {instructor.apellidos}"
            instructor.delete()
            messages.success(self.request, f'¡Éxito! El instructor {nombre_completo} ha sido eliminado correctamente.')
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            messages.error(self.request, 'No se pudo eliminar el instructor. Puede que tenga registros asociados.')
            return HttpResponseRedirect(self.success_url)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

# Vistas para ProgramaFormacion
class ProgramaFormacionListView(LoginRequiredMixin, ListView):
    model = ProgramaFormacion
    template_name = 'horarios/programasformacion/programa_formacion_list.html'
    context_object_name = 'programas'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '').strip()
        jornada = self.request.GET.get('jornada', None)

        if search_query:
            queryset = queryset.filter(
                Q(nombre_programa__icontains=search_query) |
                Q(codigo_programa__icontains=search_query)
            )
        
        if jornada:
            queryset = queryset.filter(jornada=jornada)
            
        return queryset.order_by('codigo_programa')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['selected_jornada'] = self.request.GET.get('jornada', '')
        return context

class ProgramaFormacionCreateView(LoginRequiredMixin, CreateView):
    model = ProgramaFormacion
    form_class = ProgramaFormacionForm
    template_name = 'horarios/programasformacion/programa_formacion_form.html'
    success_url = reverse_lazy('programa_formacion_list')

class ProgramaFormacionUpdateView(LoginRequiredMixin, UpdateView):
    model = ProgramaFormacion
    form_class = ProgramaFormacionForm
    template_name = 'horarios/programasformacion/programa_formacion_form.html'
    success_url = reverse_lazy('programa_formacion_list')

class ProgramaFormacionDeleteView(LoginRequiredMixin, DeleteView):
    model = ProgramaFormacion
    template_name = 'horarios/programasformacion/programa_formacion_confirm_delete.html'
    success_url = reverse_lazy('programa_formacion_list')

# Vistas para Ambiente
class AmbienteListView(LoginRequiredMixin, ListView):
    model = Ambiente
    template_name = 'horarios/ambientes/ambiente_list.html'
    context_object_name = 'ambientes'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        sede = self.request.GET.get('sede')

        # Filtrar por código o nombre de ambiente
        if query:
            queryset = queryset.filter(
                Q(codigo_ambiente__icontains=query) |
                Q(nombre_ambiente__icontains=query)
            )

        # Filtrar por sede
        if sede:
            queryset = queryset.filter(sede=sede)

        return queryset.order_by('codigo_ambiente')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        context['selected_sede'] = self.request.GET.get('sede', '')
        return context

class AmbienteCreateView(LoginRequiredMixin, CreateView):
    model = Ambiente
    form_class = AmbienteForm
    template_name = 'horarios/ambientes/ambiente_form.html'
    success_url = reverse_lazy('ambiente_list')

class AmbienteUpdateView(LoginRequiredMixin, UpdateView):
    model = Ambiente
    form_class = AmbienteForm
    template_name = 'horarios/ambientes/ambiente_form.html'
    success_url = reverse_lazy('ambiente_list')

class AmbienteDeleteView(LoginRequiredMixin, DeleteView):
    model = Ambiente
    template_name = 'horarios/ambientes/ambiente_confirm_delete.html'
    success_url = reverse_lazy('ambiente_list')

# Vistas para Competencia
class CompetenciaListView(LoginRequiredMixin, ListView):
    model = Competencia
    template_name = 'horarios/competencias/competencia_list.html'
    context_object_name = 'competencias'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        # Filtrar por código de norma si se ingresó un valor
        if query:
            queryset = queryset.filter(codigo_norma__icontains=query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CompetenciaForm()
        return context

class CompetenciaCreateView(LoginRequiredMixin, CreateView):
    model = Competencia
    form_class = CompetenciaForm
    template_name = 'horarios/competencias/competencia_form.html'
    success_url = reverse_lazy('competencia_list')

class CompetenciaUpdateView(LoginRequiredMixin, UpdateView):
    model = Competencia
    form_class = CompetenciaForm
    template_name = 'horarios/competencias/competencia_form.html'
    success_url = reverse_lazy('competencia_list')

class CompetenciaDeleteView(LoginRequiredMixin, DeleteView):
    model = Competencia
    template_name = 'horarios/competencias/competencia_confirm_delete.html'
    success_url = reverse_lazy('competencia_list')

#VISTAS PARA LOS CALENDARIOS
#Vistas para crear calendarios desde cero
class CalendarListView(LoginRequiredMixin, ListView):
    model = Calendar
    template_name = 'horarios/calendar/calendar_list.html'
    context_object_name = 'calendar'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CalendarForm()
        return context

class CalendarCreateView(LoginRequiredMixin, CreateView):
    model = Calendar
    form_class = CalendarForm
    template_name = 'horarios/calendar/calendar_form.html'
    success_url = reverse_lazy('calendar_list')

class CalendarUpdateView(LoginRequiredMixin, UpdateView):
    model = Calendar
    form_class = CalendarForm
    template_name = 'horarios/calendar/calendar_form.html'
    success_url = reverse_lazy('calendar_list')

class CalendarDeleteView(LoginRequiredMixin, DeleteView):
    model = Calendar
    template_name = 'horarios/calendar/calendar_confirm_delete.html'
    success_url = reverse_lazy('calendar_list')

#Vistas para el calendario de los instructores
class CalInstListView(LoginRequiredMixin, ListView):
    model = Calendar
    template_name = 'horarios/calinst/calinst_list.html'
    context_object_name = 'calinsts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CalInstForm()
        return context

class CalInstCreateView(LoginRequiredMixin, CreateView):
    model = Calendar
    form_class = CalInstForm
    template_name = 'horarios/calinst/calinst_form.html'
    success_url = reverse_lazy('calinst_list')

class CalInstUpdateView(LoginRequiredMixin, UpdateView):
    model = Calendar
    form_class = CalInstForm
    template_name = 'horarios/calinst/calinst_form.html'
    success_url = reverse_lazy('calinst_list')

class CalInstDeleteView(LoginRequiredMixin, DeleteView):
    model = Calendar
    template_name = 'horarios/calinst/calinst_confirm_delete.html'
    success_url = reverse_lazy('calinst_list')


    #Vistas para el calendario de los ambientes
class CalAmbListView(LoginRequiredMixin, ListView):
    model = Calendar
    template_name = 'horarios/calamb/calamb_list.html'
    context_object_name = 'calambs'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CalAmbForm()
        return context

class CalAmbCreateView(LoginRequiredMixin, CreateView):
    model = Calendar
    form_class = CalAmbForm
    template_name = 'horarios/calamb/calamb_form.html'
    success_url = reverse_lazy('calamb_list')

class CalAmbUpdateView(LoginRequiredMixin, UpdateView):
    model = Calendar
    form_class = CalAmbForm
    template_name = 'horarios/calamb/calamb_form.html'
    success_url = reverse_lazy('calamb_list')

class CalAmbDeleteView(LoginRequiredMixin, DeleteView):
    model = Calendar
    template_name = 'horarios/calamb/calamb_confirm_delete.html'
    success_url = reverse_lazy('calamb_list')

#Vistas para el calendario de los programas de formacion
class CalPFListView(LoginRequiredMixin, ListView):
    model = Calendar
    template_name = 'horarios/calpf/calpf_list.html'
    context_object_name = 'calpfs'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CalAmbForm()
        return context

class CalPFCreateView(LoginRequiredMixin, CreateView):
    model = Calendar
    form_class = CalPFForm
    template_name = 'horarios/calpf/calpf_form.html'
    success_url = reverse_lazy('calpf_list')

class CalPFUpdateView(LoginRequiredMixin, UpdateView):
    model = Calendar
    form_class = CalPFForm
    template_name = 'horarios/calpf/calpf_form.html'
    success_url = reverse_lazy('calpf_list')

class CalPFDeleteView(LoginRequiredMixin, DeleteView):
    model = Calendar
    template_name = 'horarios/calpf/calpf_confirm_delete.html'
    success_url = reverse_lazy('calpf_list')


# Vista para el Login
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
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
    administrador = request.user
    nombre_completo = f"{administrador.nombres} {administrador.apellidos}"

    # Contar el número de registros en cada modelo
    total_administradores = Administrador.objects.count()
    total_instructores = Instructor.objects.count()
    total_programas = ProgramaFormacion.objects.count()
    total_competencias = Competencia.objects.count()

    current_date = date.today()

    # Pasar los datos al template
    return render(request, 'horarios/admin_dashboard.html', {
        'admin_name': nombre_completo,
        'total_administradores': total_administradores,
        'total_instructores': total_instructores,
        'total_programas': total_programas,
        'total_competencias': total_competencias,
        'current_date': current_date
    })

# Vista para obtener todos los eventos
def get_all_events(request):
    events = []

    # Obtener eventos de Instructores
    instructors = Instructor.objects.all()
    for instructor in instructors:
        events.append({
            'id_instructor': instructor.id,
            'instructor': instructor.nombres + ' ' + instructor.apellidos,
        })

    # Obtener eventos de Programas de Formación
    programas = ProgramaFormacion.objects.all()
    for programa in programas:
        events.append({
            'id_programa': programa.id,
            'programa': programa.codigo_programa + ' - ' + programa.nombre_programa,
        })

    # Obtener eventos de Ambientes
    ambientes = Ambiente.objects.all()
    for ambiente in ambientes:
        events.append({
            'id_ambiente': ambiente.id,
            'ambiente': ambiente.codigo_ambiente + ' - ' + ambiente.nombre_ambiente,
        })

    return JsonResponse(events, safe=False)

#para que se puedan cargar instructores con un archivo csv
from django.shortcuts import redirect
from django.contrib import messages
import csv
from .models import Instructor

def upload_instructors_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES['file']

        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'El archivo debe ser en formato CSV.')
            return redirect('instructor_list')

        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.reader(decoded_file)
        next(reader)  # Ignora el encabezado

        for row in reader:
            if len(row) < 6:
                messages.error(request, 'Faltan datos en una de las filas.')
                continue

            # Crea el instructor
            Instructor.objects.create(
                nombres=row[0],
                apellidos=row[1],
                correo_institucional=row[2],
                numero_celular=row[3],
                numero_cedula=row[4],
                competencias_imparte=row[5],
            )

        messages.success(request, 'Instructores cargados correctamente.')
        return redirect('instructor_list')

    return redirect('instructor_list')  # En caso de que no sea un POST

def upload_instructors_excel(request):
    if request.method == 'POST':
        if 'file' not in request.FILES:
            messages.error(request, 'Por favor, selecciona un archivo Excel.')
            return redirect('instructor_list')
            
        excel_file = request.FILES['file']
        
        if not excel_file.name.endswith(('.xlsx', '.xls')):
            messages.error(request, 'El archivo debe ser Excel (.xlsx o .xls)')
            return redirect('instructor_list')
            
        try:
            df = pd.read_excel(excel_file)
            required_columns = ['nombres', 'apellidos', 'correo_institucional', 
                              'numero_celular', 'numero_cedula']
            
            df.columns = df.columns.str.lower()
            
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                messages.error(request, 
                    f'El archivo no contiene las siguientes columnas requeridas: {", ".join(missing_columns)}')
                return redirect('instructor_list')
            
            success_count = 0
            error_count = 0
            
            for index, row in df.iterrows():
                try:
                    # Validaciones mejoradas
                    nombres = str(row['nombres']).strip()
                    apellidos = str(row['apellidos']).strip()
                    correo = str(row['correo_institucional']).strip()
                    celular = str(row['numero_celular']).strip()
                    cedula = str(row['numero_cedula']).strip()
                    
                    if not all([nombres, apellidos, correo, celular, cedula]):
                        raise ValidationError('Todos los campos son obligatorios')
                    
                    if not correo.endswith('@sena.edu.co'):
                        raise ValidationError('El correo debe ser institucional (@sena.edu.co)')
                    
                    if len(str(celular)) != 10:
                        raise ValidationError('El número de celular debe tener 10 dígitos')
                    
                    Instructor.objects.create(
                        nombres=nombres,
                        apellidos=apellidos,
                        correo_institucional=correo,
                        numero_celular=celular,
                        numero_cedula=cedula
                    )
                    success_count += 1
                    
                except Exception as e:
                    error_count += 1
                    error_msg = str(e)
                    if "Duplicate entry" in error_msg:
                        error_msg = f"La cédula '{cedula}' ya está registrada"
                    messages.error(request, f"Fila {index + 2}: {error_msg}")
                    continue
            
            if success_count > 0:
                messages.success(request, 
                    f'¡Éxito! Se importaron {success_count} instructores correctamente.')
            if error_count > 0:
                messages.warning(request, 
                    f'No se pudieron importar {error_count} registros. Revisa los errores mostrados.')
                
        except Exception as e:
            messages.error(request, f'Error al procesar el archivo: {str(e)}')
            
        return redirect('instructor_list')
    
    return redirect('instructor_list')

def download_instructor_template(request):
    # Crear la plantilla
    template_path = create_instructor_template()
    
    # Abrir el archivo
    file = open(template_path, 'rb')
    
    # Crear la respuesta
    response = FileResponse(
        file,
        as_attachment=True,
        filename='plantilla_instructores.xlsx'
    )
    
    return response

@login_required
@require_POST
def delete_all_instructors(request):
    try:
        # Obtener el número total de instructores antes de eliminar
        total_instructores = Instructor.objects.count()
        
        # Eliminar todos los instructores
        Instructor.objects.all().delete()
        
        # Devolver respuesta exitosa
        return JsonResponse({
            'status': 'success',
            'message': f'Se eliminaron {total_instructores} instructores exitosamente'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

@login_required
def crear_instructor(request):
    # Aquí irá la lógica para crear un instructor
    return render(request, 'horarios/crear_instructor.html')

@login_required
def programa_form(request):
    if request.method == 'POST':
        form = ProgramaFormacionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Programa de formación creado exitosamente.')
            return redirect('programa_formacion_list')
    else:
        form = ProgramaFormacionForm()
    
    context = {
        'form': form,
        'title': 'Crear Nuevo Programa de Formación'
    }
    return render(request, 'horarios/programasformacion/programa_formacion_form.html', context)

@login_required
def crear_competencia(request):
    # Aquí irá la lógica para crear una competencia
    return render(request, 'horarios/crear_competencia.html')

@login_required
def generar_horario(request):
    # Aquí irá la lógica para generar horarios
    return render(request, 'horarios/generar_horario.html')

@login_required
def instructor_form(request):
    if request.method == 'POST':
        form = InstructorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Instructor creado exitosamente.')
            return redirect('instructor_list')
    else:
        form = InstructorForm()
    
    context = {
        'form': form,
        'title': 'Crear Nuevo Instructor'
    }
    return render(request, 'horarios/instructores/instructor_form.html', context)

@login_required
def competencia_form(request):
    if request.method == 'POST':
        form = CompetenciaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Competencia creada exitosamente.')
            return redirect('competencia_list')
    else:
        form = CompetenciaForm()
    
    context = {
        'form': form,
        'title': 'Crear Nueva Competencia'
    }
    return render(request, 'horarios/competencias/competencia_form.html', context)

@login_required
def horario_form(request):
    return render(request, 'horarios/horarios/horario_form.html')