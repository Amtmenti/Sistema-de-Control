import json
from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import DeleteView, CreateView, UpdateView, TemplateView
from django.forms import model_to_dict
from core.pos.forms import AlumnoForm
from core.pos.models import Alumno
from core.security.mixins import GroupPermissionMixin

MODULE_NAME = 'Alumnos'

class AlumnoListView(GroupPermissionMixin, TemplateView):
    template_name = 'alumno/list.html'
    permission_required = 'view_alumno'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                for i in Alumno.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Alumnos'
        context['list_url'] = reverse_lazy('alumno_list')
        context['create_url'] = reverse_lazy('alumno_create')
        context['module_name'] = MODULE_NAME
        user = self.request.user
        if user.groups.filter(name='Administrador').exists():
            context['user_type'] = 'Administrador'
        elif user.groups.filter(name='Alumno').exists():
            context['user_type'] = 'Alumno'
        return context


class AlumnoCreateView(GroupPermissionMixin, CreateView):
    template_name = 'alumno/create.html'
    model = Alumno
    form_class = AlumnoForm
    success_url = reverse_lazy('alumno_list')
    permission_required = 'add_alumno'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST.get('action')
        try:
            if action == 'add':
                form = self.get_form()
                if form.is_valid():
                    alumno = form.save(commit=False)
                    alumno.save()
                    messages.success(request, 'Alumno creado exitosamente.')
                    data = alumno.toJSON()
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
        context['title'] = 'Nuevo registro de un Alumno'
        context['action'] = 'add'
        context['module_name'] = MODULE_NAME
        user = self.request.user
        if user.groups.filter(name='Administrador').exists():
            context['user_type'] = 'Administrador'
        elif user.groups.filter(name='Alumno').exists():
            context['user_type'] = 'Alumno'
        return context


class AlumnoUpdateView(GroupPermissionMixin, UpdateView):
    template_name = 'alumno/create.html'
    model = Alumno
    form_class = AlumnoForm
    success_url = reverse_lazy('alumno_list')
    permission_required = 'change_alumno'

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
                    alumno = form.save(commit=False)
                    alumno.save()
                    messages.success(request, 'Alumno actualizado exitosamente.')
                    data = alumno.toJSON()
                else:
                    data['error'] = form.errors
                    messages.error(request, 'Error al actualizar el alumno.')
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
        context['title'] = 'Edición de un Alumno'
        context['action'] = 'edit'
        context['module_name'] = MODULE_NAME
        user = self.request.user
        if user.groups.filter(name='Administrador').exists():
            context['user_type'] = 'Administrador'
        elif user.groups.filter(name='Alumno').exists():
            context['user_type'] = 'Alumno'
        return context


class AlumnoDeleteView(GroupPermissionMixin, DeleteView):
    model = Alumno
    template_name = 'delete.html'
    success_url = reverse_lazy('alumno_list')
    permission_required = 'delete_alumno'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.get_object().delete()
            messages.success(request, 'Alumno eliminado exitosamente.')
        except Exception as e:
            data['error'] = str(e)
            messages.error(request, 'Error: ' + str(e))
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de un Alumno'
        context['list_url'] = self.success_url
        context['module_name'] = MODULE_NAME
        user = self.request.user
        if user.groups.filter(name='Administrador').exists():
            context['user_type'] = 'Administrador'
        elif user.groups.filter(name='Alumno').exists():
            context['user_type'] = 'Alumno'
        return context
