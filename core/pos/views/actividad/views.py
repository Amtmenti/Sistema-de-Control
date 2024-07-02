import json
from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import DeleteView, CreateView, UpdateView, TemplateView
from core.pos.forms import ActividadForm
from core.pos.models import Actividad
from core.security.mixins import GroupPermissionMixin

MODULE_NAME = 'Actividades'

class ActividadListView(GroupPermissionMixin, TemplateView):
    template_name = 'actividad/list.html'
    permission_required = 'view_actividad'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST.get('action')
        try:
            if action == 'search':
                data = []
                for i in Actividad.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Actividades'
        context['list_url'] = reverse_lazy('actividad_list')
        context['create_url'] = reverse_lazy('actividad_create')
        context['module_name'] = MODULE_NAME
        user = self.request.user
        if user.groups.filter(name='Administrador').exists():
            context['user_type'] = 'Administrador'
        elif user.groups.filter(name='Alumno').exists():
            context['user_type'] = 'Alumno'
        return context


class ActividadCreateView(GroupPermissionMixin, CreateView):
    template_name = 'actividad/create.html'
    model = Actividad
    form_class = ActividadForm
    success_url = reverse_lazy('actividad_list')
    permission_required = 'add_actividad'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST.get('action')
        try:
            if action == 'add':
                form = self.get_form()
                if form.is_valid():
                    actividad = form.save(commit=False)
                    actividad.save(user=request.user)
                    messages.success(request, 'Actividad creada exitosamente.')
                    data = actividad.toJSON()
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
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_url'] = self.success_url
        context['title'] = 'Nueva Actividad'
        context['action'] = 'add'
        context['module_name'] = MODULE_NAME
        user = self.request.user
        if user.groups.filter(name='Administrador').exists():
            context['user_type'] = 'Administrador'
        elif user.groups.filter(name='Alumno').exists():
            context['user_type'] = 'Alumno'
        return context


class ActividadUpdateView(GroupPermissionMixin, UpdateView):
    template_name = 'actividad/create.html'
    model = Actividad
    form_class = ActividadForm
    success_url = reverse_lazy('actividad_list')
    permission_required = 'change_actividad'

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
                    actividad = form.save(commit=False)
                    actividad.save(user=request.user)
                    messages.success(request, 'Actividad actualizada exitosamente.')
                    data = actividad.toJSON()
                else:
                    data['error'] = form.errors
                    messages.error(request, 'Error al actualizar la actividad.')
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
        context['title'] = 'Edición de una Actividad'
        context['action'] = 'edit'
        context['module_name'] = MODULE_NAME
        user = self.request.user
        if user.groups.filter(name='Administrador').exists():
            context['user_type'] = 'Administrador'
        elif user.groups.filter(name='Alumno').exists():
            context['user_type'] = 'Alumno'
        return context


class ActividadDeleteView(GroupPermissionMixin, DeleteView):
    model = Actividad
    template_name = 'delete.html'
    success_url = reverse_lazy('actividad_list')
    permission_required = 'delete_actividad'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.get_object().delete()
            messages.success(request, 'Actividad eliminada exitosamente.')
        except Exception as e:
            data['error'] = str(e)
            messages.error(request, 'Error: ' + str(e))
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de una Actividad'
        context['list_url'] = self.success_url
        context['module_name'] = MODULE_NAME
        user = self.request.user
        if user.groups.filter(name='Administrador').exists():
            context['user_type'] = 'Administrador'
        elif user.groups.filter(name='Alumno').exists():
            context['user_type'] = 'Alumno'
        return context
