import json
from decimal import Decimal
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic import FormView
from core.pos.models import Alumno, RegistroEntrada, RegistroSalida
from core.reports.forms import AlumnoReportForm

MODULE_NAME = 'R.Alumno'

def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

class AlumnoReportView(LoginRequiredMixin, FormView):
    template_name = 'alumno_report/report.html'
    form_class = AlumnoReportForm

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        data = {}
        try:
            if action == 'search_report':
                data = []
                alumno_id = request.POST.get('alumno')
                if alumno_id:
                    queryset_entrada = RegistroEntrada.objects.filter(alumno_id=alumno_id).order_by('fecha', 'hora_entrada')
                    for entrada in queryset_entrada:
                        salidas = RegistroSalida.objects.filter(alumno_id=alumno_id, fecha=entrada.fecha, hora_salida__gte=entrada.hora_entrada).order_by('hora_salida')
                        if salidas.exists():
                            salida = salidas.first()  # Obtener la primera salida después de la entrada
                            item = {
                                'alumno': entrada.alumno.toJSON(),
                                'fecha': entrada.fecha.strftime('%Y-%m-%d'),
                                'hora_entrada': entrada.hora_entrada.strftime('%H:%M'),
                                'hora_salida': salida.hora_salida.strftime('%H:%M'),
                                'descripcion_actividad': salida.descripcion_actividad,
                                'total_horas': salida.total_horas if salida.total_horas else '00:00',
                            }
                            data.append(item)
            else:
                data = {'error': 'No ha seleccionado ninguna opción'}
        except Exception as e:
            data = {'error': str(e)}
        return HttpResponse(json.dumps(data, default=decimal_default), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte por Alumno'
        context['module_name'] = MODULE_NAME
        user = self.request.user
        if user.groups.filter(name='Administrador').exists():
            context['user_type'] = 'Administrador'
        elif user.groups.filter(name='Alumno').exists():
            context['user_type'] = 'Alumno'
        return context
