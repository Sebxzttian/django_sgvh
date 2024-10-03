# calendarios/views.py

from django.shortcuts import render
from .models import Calendar
from django.http import JsonResponse

def cal_eventos(request):
    # Renderiza la plantilla principal del calendario
    return render(request, 'calendarios/cal_eventos.html')

def get_all_events(request):
    events = Calendar.objects.all()
    event_list = []
    for event in events:
        event_list.append({
            'start': event.start.isoformat(),
            'end': event.end.isoformat(),
            'instructor': event.nombres_instructor,
            'programa': event.nombre_programa,
            'ambiente': event.nombre_ambiente,
            'competencia': event.nombre_competencia,
            'norma_competencia': event.norma_competencia,
        })
    return JsonResponse(event_list, safe=False)
