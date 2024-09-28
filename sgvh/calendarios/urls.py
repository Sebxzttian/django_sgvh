# calendarios/urls.py

from django.urls import path
from .views import calinst, calamb, calpf, get_instructor_events, get_programa_events, get_ambiente_events

urlpatterns = [
    path('calinst/', calinst, name='calinst'),
    path('calamb/', calamb, name='calamb'),
    path('calpf/', calpf, name='calpf'),
    
    # Rutas para obtener eventos
    path('get_instructor_events/<int:id>/', get_instructor_events, name='get_instructor_events'),
    path('get_programa_events/<int:id>/', get_programa_events, name='get_programa_events'),
    path('get_ambiente_events/<int:id>/', get_ambiente_events, name='get_ambiente_events'),
]
