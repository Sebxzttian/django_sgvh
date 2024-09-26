from django.shortcuts import render
from .models import CalIns

def CalInstListView(request):
    calendarios = CalIns.objects.all()
    return render(request, 'calendarios/calinst_list.html', {'calendarios': calendarios})
