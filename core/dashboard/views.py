import json
from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import FloatField, Sum
from django.db.models.functions import Coalesce
from django.http import HttpResponse
from django.views.generic import TemplateView

from core.pos.models import RegistroEntrada, RegistroSalida, Alumno
from core.security.models import Dashboard

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'panel.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Panel de Administración'
        context['dashboard'] = Dashboard.objects.first()
        user = self.request.user

        # Añadir los registros de entrada y salida al contexto
        context['registroentradas'] = RegistroEntrada.objects.order_by('-fecha', '-hora_entrada')[:10]
        context['registrosalidas'] = RegistroSalida.objects.order_by('-fecha', '-hora_salida')[:10]

        if user.groups.filter(name='Administrador').exists():
            context['user_type'] = 'Administrador'
        elif user.groups.filter(name='Alumno').exists():
            context['user_type'] = 'Alumno'
        return context
