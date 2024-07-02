import json
from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import DeleteView, CreateView, UpdateView, TemplateView
from core.pos.forms import HorarioForm
from core.pos.models import Horario
from core.security.mixins import GroupPermissionMixin

MODULE_NAME = 'Horarios'

class HorarioListView(GroupPermissionMixin, TemplateView):
    template_name = 'horario/list.html'
    permission_required = 'view_horario'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                for i in Horario.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Horarios'
        context['list_url'] = reverse_lazy('horario_list')
        context['create_url'] = reverse_lazy('horario_create')
        context['module_name'] = MODULE_NAME
        user = self.request.user
        if user.groups.filter(name='Administrador').exists():
            context['user_type'] = 'Administrador'
        elif user.groups.filter(name='Alumno').exists():
            context['user_type'] = 'Alumno'
        return context

class HorarioCreateView(GroupPermissionMixin, CreateView):
    template_name = 'horario/create.html'
    model = Horario
    form_class = HorarioForm
    success_url = reverse_lazy('horario_list')
    permission_required = 'add_horario'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST.get('action')
        try:
            if action == 'add':
                form = self.get_form()
                if form.is_valid():
                    horario = form.save()
                    messages.success(request, 'Horario creado exitosamente.')
                    data = horario.toJSON()
                else:
                    data['error'] = form.errors
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de un Horario'
        context['action'] = 'add'
        user = self.request.user
        if user.groups.filter(name='Administrador').exists():
            context['user_type'] = 'Administrador'
        elif user.groups.filter(name='Alumno').exists():
            context['user_type'] = 'Alumno'
        return context


class HorarioUpdateView(GroupPermissionMixin, UpdateView):
    template_name = 'horario/create.html'
    model = Horario
    form_class = HorarioForm
    success_url = reverse_lazy('horario_list')
    permission_required = 'change_horario'

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
                    horario = form.save(commit=False)
                    horario.save()
                    messages.success(request, 'Horario actualizado exitosamente.')
                    data = horario.toJSON()
                else:
                    errors = []
                    for field, error_list in form.errors.items():
                        for error in error_list:
                            errors.append(error)
                    data['error'] = errors
                    for error in errors:
                        messages.error(request, error)
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
                messages.error(request, 'No ha seleccionado ninguna opción.')
        except Exception as e:
            data['error'] = str(e)
            messages.error(request, 'Error: ' + str(e))
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_url'] = self.success_url
        context['title'] = 'Edición de un Horario'
        context['action'] = 'edit'
        context['module_name'] = MODULE_NAME
        user = self.request.user
        if user.groups.filter(name='Administrador').exists():
            context['user_type'] = 'Administrador'
        elif user.groups.filter(name='Alumno').exists():
            context['user_type'] = 'Alumno'
        return context


class HorarioDeleteView(GroupPermissionMixin, DeleteView):
    model = Horario
    template_name = 'delete.html'
    success_url = reverse_lazy('horario_list')
    permission_required = 'delete_horario'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.get_object().delete()
            messages.success(request, 'Horario eliminado exitosamente.')
        except Exception as e:
            data['error'] = str(e)
            messages.error(request, 'Error: ' + str(e))
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de un Horario'
        context['list_url'] = self.success_url
        context['module_name'] = MODULE_NAME
        user = self.request.user
        if user.groups.filter(name='Administrador').exists():
            context['user_type'] = 'Administrador'
        elif user.groups.filter(name='Alumno').exists():
            context['user_type'] = 'Alumno'
        return context
