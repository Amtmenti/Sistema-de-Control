import json
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView
from core.pos.forms import AsignacionHorasForm
from core.pos.models import RegistroEntrada, RegistroSalida
from django.contrib.auth.mixins import LoginRequiredMixin

MODULE_NAME = 'Registros de Entrada y Salida'

class RegistroEntradaSalidaListView(LoginRequiredMixin, TemplateView):
    template_name = 'registrocombinado/list.html'

    def post(self, request, *args, **kwargs):
        data = []
        action = request.POST.get('action')
        try:
            if action == 'search':
                registros_entrada = RegistroEntrada.objects.all()
                registros_salida = RegistroSalida.objects.all()

                for entrada in registros_entrada:
                    salida = registros_salida.filter(alumno=entrada.alumno, fecha=entrada.fecha).first()
                    if salida:
                        item = {
                            'alumno': entrada.alumno.nombre_completo,
                            'hora_entrada': entrada.hora_entrada.strftime('%H:%M'),
                            'hora_salida': salida.hora_salida.strftime('%H:%M'),
                            'fecha': entrada.fecha.strftime('%Y-%m-%d'),
                            'descripcion_actividad': salida.descripcion_actividad,
                            'total_horas': salida.total_horas,
                        }
                        data.append(item)
            else:
                data = {'error': 'No ha seleccionado ninguna opción'}
        except Exception as e:
            data = {'error': str(e)}
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Registros de Entrada y Salida'
        context['list_url'] = reverse_lazy('registro_entrada_salida_list')
        context['create_url'] = reverse_lazy('registro_entrada_salida_create')
        context['module_name'] = MODULE_NAME
        user = self.request.user
        if user.groups.filter(name='Administrador').exists():
            context['user_type'] = 'Administrador'
        elif user.groups.filter(name='Alumno').exists():
            context['user_type'] = 'Alumno'
        return context

class RegistroEntradaSalidaCreateView(LoginRequiredMixin, FormView):
    template_name = 'registrocombinado/create.html'
    form_class = AsignacionHorasForm
    success_url = reverse_lazy('registro_entrada_salida_list')

    def form_valid(self, form):
        try:
            entrada, salida = form.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    def form_invalid(self, form):
        return JsonResponse({'success': False, 'errors': form.errors.as_json()})

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de entrada y salida'
        context['action'] = 'add'
        context['module_name'] = MODULE_NAME
        user = self.request.user
        if user.groups.filter(name='Administrador').exists():
            context['user_type'] = 'Administrador'
        elif user.groups.filter(name='Alumno').exists():
            context['user_type'] = 'Alumno'
        return context
