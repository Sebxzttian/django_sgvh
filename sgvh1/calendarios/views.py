# calendarios/views.py

from django.shortcuts import render
from .models import CalInst, CalPF, CalAmb  # Asegúrate de importar los modelos adecuados
from horarios.models import Ambiente, ProgramaFormacion, Instructor  # Importa los modelos necesarios de 'horarios'
import json
from django.http import JsonResponse

def calinst(request):
    instructores = Instructor.objects.all()  # Obtener todos los instructores
    return render(request, 'calendarios/calinst.html', {'instructores': instructores})

def calamb(request):
    ambientes = Ambiente.objects.all()  # Obtener todos los ambientes
    return render(request, 'calendarios/calamb.html', {'ambientes': ambientes})

def calpf(request):
    programas = ProgramaFormacion.objects.all()  # Obtener todos los programas
    return render(request, 'calendarios/calpf.html', {'programas': programas})


#events
def get_instructor_events(request, id):
    events = CalInst.objects.filter(instructor_id=id)
    event_list = []
    for event in events:
        event_list.append({
            'start': event.fecha_inicio.isoformat(),
            'end': event.fecha_fin.isoformat(),
            'programa': event.programa.nombre_programa,
            'codigo_programa': event.programa.codigo_programa,
            'ambiente': event.ambiente.nombre_ambiente,
            'codigo_ambiente': event.ambiente.codigo_ambiente,
            'competencia': event.competencia.nombre,
            'norma_competencia': event.competencia.codigo_norma,
        })
    return JsonResponse(event_list, safe=False)

def get_programa_events(request, id):
    events = CalPF.objects.filter(programa_id=id)
    event_list = []
    for event in events:
        event_list.append({
            'start': event.fecha_inicio.isoformat(),
            'end': event.fecha_fin.isoformat(),
            'instructor': event.instructor.nombres,
            'apellido_instructor': event.instructor.apellidos,
            'ambiente': event.ambiente.nombre_ambiente,
            'codigo_ambiente': event.ambiente.codigo_ambiente,
            'competencia': event.competencia.nombre,
            'norma_competencia': event.competencia.codigo_norma,
        })
    return JsonResponse(event_list, safe=False)

def get_ambiente_events(request, id):
    events = CalAmb.objects.filter(ambiente_id=id)
    event_list = []
    for event in events:
        event_list.append({
            'start': event.fecha_inicio.isoformat(),
            'end': event.fecha_fin.isoformat(),
            'instructor': event.instructor.nombres,
            'apellido_instructor': event.instructor.apellidos,
            'programa': event.programa.nombre_programa,
            'codigo_programa': event.programa.codigo_programa,
            'competencia': event.competencia.nombre,
            'norma_competencia': event.competencia.codigo_norma,
        })
    return JsonResponse(event_list, safe=False)
