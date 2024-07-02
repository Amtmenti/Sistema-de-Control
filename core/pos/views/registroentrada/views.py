import json
from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import DeleteView, CreateView, UpdateView, TemplateView
from core.pos.forms import RegistroEntradaForm
from core.pos.models import RegistroEntrada
from core.security.mixins import GroupPermissionMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

MODULE_NAME = 'Registro de Entrada'

class RegistroEntradaListView(GroupPermissionMixin, TemplateView):
    template_name = 'registroentrada/list.html'
    permission_required = 'view_registroentrada'

    def post(self, request, *args, **kwargs):
        data = []
        action = request.POST.get('action')
        try:
            if action == 'search':
                for i in RegistroEntrada.objects.all():
                    data.append(i.toJSON())
            else:
                data.append({'error': 'No ha seleccionado ninguna opción'})
        except Exception as e:
            data.append({'error': str(e)})
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Registro de Entrada'
        context['list_url'] = reverse_lazy('registroentrada_list')
        context['create_url'] = reverse_lazy('registroentrada_create')
        context['module_name'] = MODULE_NAME
        user = self.request.user
        if user.groups.filter(name='Administrador').exists():
            context['user_type'] = 'Administrador'
        elif user.groups.filter(name='Alumno').exists():
            context['user_type'] = 'Alumno'
        return context

class RegistroEntradaCreateView(LoginRequiredMixin, GroupPermissionMixin, CreateView):
    template_name = 'registroentrada/create.html'
    model = RegistroEntrada
    form_class = RegistroEntradaForm
    success_url_admin = reverse_lazy('registroentrada_list')
    success_url_alumno = reverse_lazy('dashboard')
    permission_required = 'add_registroentrada'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['is_edit'] = False
        return kwargs

    def form_valid(self, form):
        registro = form.save(commit=False)
        registro.save()
        messages.success(self.request, 'Registro de entrada creado exitosamente.')
        
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
        context['title'] = 'Nuevo registro de entrada'
        context['action'] = 'add'
        context['module_name'] = MODULE_NAME
        user = self.request.user
        if user.groups.filter(name='Administrador').exists():
            context['user_type'] = 'Administrador'
        elif user.groups.filter(name='Alumno').exists():
            context['user_type'] = 'Alumno'
        return context


class RegistroEntradaUpdateView(GroupPermissionMixin, UpdateView):
    template_name = 'registroentrada/create.html'
    model = RegistroEntrada
    form_class = RegistroEntradaForm
    success_url = reverse_lazy('registroentrada_list')
    permission_required = 'change_registroentrada'

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
                    messages.success(request, 'Registro de entrada actualizado exitosamente.')
                    data = registro.toJSON()
                else:
                    data['error'] = form.errors
                    messages.error(request, 'Error al actualizar el registro de entrada.')
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
        context['title'] = 'Edición de un registro de entrada'
        context['action'] = 'edit'
        context['module_name'] = MODULE_NAME
        user = self.request.user
        if user.groups.filter(name='Administrador').exists():
            context['user_type'] = 'Administrador'
        elif user.groups.filter(name='Alumno').exists():
            context['user_type'] = 'Alumno'
        return context


class RegistroEntradaDeleteView(GroupPermissionMixin, DeleteView):
    model = RegistroEntrada
    template_name = 'delete.html'
    success_url = reverse_lazy('registroentrada_list')
    permission_required = 'delete_registroentrada'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.get_object().delete()
            messages.success(request, 'Registro de entrada eliminado exitosamente.')
        except Exception as e:
            data['error'] = str(e)
            messages.error(request, 'Error: ' + str(e))
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de un registro de entrada'
        context['list_url'] = self.success_url
        context['module_name'] = MODULE_NAME
        user = self.request.user
        if user.groups.filter(name='Administrador').exists():
            context['user_type'] = 'Administrador'
        elif user.groups.filter(name='Alumno').exists():
            context['user_type'] = 'Alumno'
        return context
