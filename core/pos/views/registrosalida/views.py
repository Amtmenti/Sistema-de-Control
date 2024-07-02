import json
from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import DeleteView, CreateView, UpdateView, TemplateView
from core.pos.forms import RegistroSalidaForm
from core.pos.models import RegistroSalida
from core.security.mixins import GroupPermissionMixin
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

MODULE_NAME = 'Registros de Salida'

class RegistroSalidaListView(GroupPermissionMixin, TemplateView):
    template_name = 'registrosalida/list.html'
    permission_required = 'view_registrosalida'

    def post(self, request, *args, **kwargs):
        data = []
        action = request.POST['action']
        try:
            if action == 'search':
                for i in RegistroSalida.objects.all():
                    data.append(i.toJSON())
            else:
                data = {'error': 'No ha seleccionado ninguna opción'}
        except Exception as e:
            data = {'error': str(e)}
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Registros de Salida'
        context['list_url'] = reverse_lazy('registrosalida_list')
        context['create_url'] = reverse_lazy('registrosalida_create')
        context['module_name'] = MODULE_NAME
        user = self.request.user
        if user.groups.filter(name='Administrador').exists():
            context['user_type'] = 'Administrador'
        elif user.groups.filter(name='Alumno').exists():
            context['user_type'] = 'Alumno'
        return context

class RegistroSalidaCreateView(GroupPermissionMixin, CreateView):
    template_name = 'registrosalida/create.html'
    model = RegistroSalida
    form_class = RegistroSalidaForm
    success_url_admin = reverse_lazy('registrosalida_list')
    success_url_alumno = reverse_lazy('dashboard')
    permission_required = 'add_registrosalida'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['is_edit'] = False
        return kwargs

    def form_valid(self, form):
        registro = form.save(commit=False)
        registro.save()
        messages.success(self.request, 'Registro de salida creado exitosamente.')

        if self.request.user.groups.filter(name='Administrador').exists():
            self.success_url = self.success_url_admin
        elif self.request.user.groups.filter(name='Alumno').exists():
            self.success_url = self.success_url_alumno
        
        response_data = {'success': True, 'redirect_url': self.success_url}
        return JsonResponse(response_data)

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST.get('action')
        try:
            if action == 'add':
                form = self.get_form()
                if form.is_valid():
                    return self.form_valid(form)
                else:
                    data['error'] = form.errors.as_json()
                    for error in form.errors.values():
                        messages.error(request, error.as_text().replace('*', ''))
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
                messages.error(request, 'No ha seleccionado ninguna opción.')
        except Exception as e:
            data['error'] = str(e)
            messages.error(request, 'Error: ' + str(e))
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_url'] = self.success_url_admin if self.request.user.groups.filter(name='Administrador').exists() else self.success_url_alumno
        context['title'] = 'Nuevo registro de salida'
        context['action'] = 'add'
        context['module_name'] = MODULE_NAME
        user = self.request.user
        if user.groups.filter(name='Administrador').exists():
            context['user_type'] = 'Administrador'
        elif user.groups.filter(name='Alumno').exists():
            context['user_type'] = 'Alumno'
        return context

class RegistroSalidaUpdateView(GroupPermissionMixin, UpdateView):
    template_name = 'registrosalida/create.html'
    model = RegistroSalida
    form_class = RegistroSalidaForm
    success_url = reverse_lazy('registrosalida_list')
    permission_required = 'change_registrosalida'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['is_edit'] = True
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'edit':
                form = self.get_form()
                if form.is_valid():
                    registro = form.save(commit=False)
                    registro.save()
                    messages.success(request, 'Registro de salida actualizado exitosamente.')
                    data = registro.toJSON()
                else:
                    data['error'] = form.errors
                    messages.error(request, 'Error al actualizar el registro de salida.')
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
                messages.error(request, 'No ha seleccionado ninguna opción.')
        except Exception as e:
            data = {'error': str(e)}
            messages.error(request, 'Error: ' + str(e))
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_url'] = self.success_url
        context['title'] = 'Edición de un registro de salida'
        context['action'] = 'edit'
        context['module_name'] = MODULE_NAME
        user = self.request.user
        if user.groups.filter(name='Administrador').exists():
            context['user_type'] = 'Administrador'
        elif user.groups.filter(name='Alumno').exists():
            context['user_type'] = 'Alumno'
        return context

class RegistroSalidaDeleteView(GroupPermissionMixin, DeleteView):
    model = RegistroSalida
    template_name = 'delete.html'
    success_url = reverse_lazy('registrosalida_list')
    permission_required = 'delete_registrosalida'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.get_object().delete()
            messages.success(request, 'Registro de salida eliminado exitosamente.')
        except Exception as e:
            data = {'error': str(e)}
            messages.error(request, 'Error: ' + str(e))
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de un registro de salida'
        context['list_url'] = self.success_url
        context['module_name'] = MODULE_NAME
        user = self.request.user
        if user.groups.filter(name='Administrador').exists():
            context['user_type'] = 'Administrador'
        elif user.groups.filter(name='Alumno').exists():
            context['user_type'] = 'Alumno'
        return context
