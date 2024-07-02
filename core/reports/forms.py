from django import forms
from core.pos.models import Alumno

class AlumnoReportForm(forms.Form):
    alumno = forms.ModelChoiceField(queryset=Alumno.objects.all(), widget=forms.Select(attrs={
        'class': 'form-control',
    }), label='Buscar por Alumno')

class ReportForm(forms.Form):
    date_range = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off'
    }), label='Buscar por rango de fechas')
