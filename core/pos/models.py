import os
import secrets
from datetime import datetime, timedelta, time
from django.db import models
from django.forms import model_to_dict
from django.core.exceptions import ValidationError
from config import settings
from core.pos.choices import Modalidad, Dias, Estados_Email
from core.user.models import User
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils.html import strip_tags


#############
# Función para generar un token único
def generate_unique_token():
    return secrets.token_urlsafe(6)[:8]

class Alumno(models.Model):
    nombre_completo = models.CharField(null=True, max_length=150, verbose_name='Nombre Completo')
    telefono_celular = models.CharField(max_length=10, null=True, blank=True, verbose_name='Teléfono Celular')
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name='Email')
    modalidad = models.CharField(max_length=50, choices=Modalidad, default=Modalidad[0][0][0], verbose_name='Modalidad')
    periodo_inicio = models.DateField(verbose_name='Fecha de Inicio')
    periodo_termino = models.DateField(verbose_name='Fecha de Término')
    token = models.CharField(default=generate_unique_token, max_length=8, unique=True, editable=True, verbose_name='Token para el Alumno')
    duracion_periodo = models.PositiveIntegerField(null=True, blank=True, verbose_name='Introduzca las horas a cubrir')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f'{self.nombre_completo} ({self.modalidad})'

    def periodo_inicio_format(self):
        return self.periodo_inicio.strftime('%Y-%m-%d')

    def periodo_termino_format(self):
        return self.periodo_termino.strftime('%Y-%m-%d')

    @property
    def duracion_periodo_format(self):
        if self.duracion_periodo is not None:
            hours, remainder = divmod(self.duracion_periodo * 60, 60)
            minutes = remainder
            return f"{int(hours)}:{int(minutes):02d}"
        return "0:00"

    @property
    def horas_cumplidas(self):
        registros_salida = RegistroSalida.objects.filter(alumno=self)
        total_horas = sum(
            float(reg.total_horas.split(':')[0]) + float(reg.total_horas.split(':')[1]) / 60
            for reg in registros_salida if reg.total_horas
        )
        return self.format_hours_minutes(total_horas)

    @property
    def horas_restantes(self):
        if self.duracion_periodo is not None:
            horas_cumplidas_float = self.total_hours_to_float(self.horas_cumplidas)
            horas_restantes_float = self.duracion_periodo - horas_cumplidas_float
            return self.format_hours_minutes(horas_restantes_float)
        return "0:00"

    def format_hours_minutes(self, decimal_hours):
        hours = int(decimal_hours)
        minutes = round((decimal_hours - hours) * 60)
        return f"{hours:02}:{minutes:02}"

    def total_hours_to_float(self, total_hours_str):
        hours, minutes = map(int, total_hours_str.split(':'))
        return hours + minutes / 60

    def toJSON(self):
        item = model_to_dict(self)
        item['text'] = self.get_full_name()
        item['modalidad'] = {'id': self.modalidad, 'name': self.get_modalidad_display()}
        item['periodo_inicio'] = self.periodo_inicio_format()
        item['periodo_termino'] = self.periodo_termino_format()
        item['token'] = self.token
        item['duracion_periodo'] = self.duracion_periodo_format if self.duracion_periodo is not None else 'null'
        item['horas_cumplidas'] = self.horas_cumplidas
        item['horas_restantes'] = self.horas_restantes
        return item

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self.generate_token()
        super().save(*args, **kwargs)

    def generate_token(self):
        return generate_unique_token()

    class Meta:
        verbose_name = 'Alumno'
        verbose_name_plural = 'Alumnos'

#########
class Horario(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='horarios')
    dia = models.CharField(max_length=10, choices=Dias, verbose_name='Día de la Semana')
    programado = models.BooleanField(default=False, verbose_name='Programado')
    hentrada = models.TimeField(null=True, verbose_name='Hora de entrada')
    hsalida = models.TimeField(null=True, verbose_name='Hora de salida')
    htotalcalc = models.CharField(max_length=5, editable=False, default='0:00', verbose_name='Total de Horas')

    def calculate_htotalcalc(self):
        if self.hentrada and self.hsalida:
            hentrada_dt = datetime.combine(datetime.min, self.hentrada)
            hsalida_dt = datetime.combine(datetime.min, self.hsalida)
            delta = hsalida_dt - hentrada_dt
            total_minutes = delta.total_seconds() / 60
            hours, minutes = divmod(total_minutes, 60)
            return f"{int(hours)}:{int(minutes):02d}"
        return "0:00"

    def save(self, *args, **kwargs):
        self.htotalcalc = self.calculate_htotalcalc()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.alumno.get_full_name()} - {self.get_dia_display()}'

    def hentrada_format(self):
        return self.hentrada.strftime('%H:%M') if self.hentrada else ''

    def hsalida_format(self):
        return self.hsalida.strftime('%H:%M') if self.hsalida else ''

    def toJSON(self):
        item = model_to_dict(self)
        item['alumno'] = self.alumno.toJSON()
        item['dia'] = self.get_dia_display()
        item['hentrada'] = self.hentrada_format()
        item['hsalida'] = self.hsalida_format()
        item['programado'] = self.programado
        item['htotalcalc'] = self.htotalcalc
        return item

    class Meta:
        verbose_name = 'Horario'
        verbose_name_plural = 'Horarios'
        unique_together = ('alumno', 'dia')  # Asegura que un alumno no pueda tener dos horarios para el mismo día


#########
def round_to_nearest_minute(t):
    # Redondea el tiempo al minuto más cercano
    return t.replace(second=0, microsecond=0)

def get_current_time():
    return round_to_nearest_minute(datetime.now().time())

def get_current_date():
    return datetime.now().date()

class RegistroEntrada(models.Model):
    alumno = models.ForeignKey('Alumno', on_delete=models.CASCADE)
    hora_entrada = models.TimeField(default=get_current_time)
    fecha = models.DateField(default=get_current_date)
    token = models.CharField(max_length=8)

    def save(self, *args, **kwargs):
        if not self.validate_token():
            raise ValueError("Token inválido")
        self.hora_entrada = round_to_nearest_minute(self.hora_entrada)
        super().save(*args, **kwargs)

    def validate_token(self):
        return self.token == self.alumno.token

    def toJSON(self):
        item = model_to_dict(self)
        item['alumno'] = self.alumno.toJSON()
        item['hora_entrada'] = self.hora_entrada.strftime('%H:%M')
        item['fecha'] = self.fecha.strftime('%Y-%m-%d')
        return item

    class Meta:
        verbose_name = 'Entrada'
        verbose_name_plural = 'Entradas'

#########
def round_to_nearest_minute(t):
    # Redondea el tiempo al minuto más cercano
    return t.replace(second=0, microsecond=0)

def get_current_time():
    return round_to_nearest_minute(datetime.now().time())

def get_current_date():
    return datetime.now().date()

class RegistroSalida(models.Model):
    alumno = models.ForeignKey('Alumno', on_delete=models.CASCADE)
    hora_salida = models.TimeField(default=get_current_time)
    fecha = models.DateField(default=get_current_date)
    token = models.CharField(max_length=8)
    descripcion_actividad = models.TextField(verbose_name='Descripción de la Actividad', null=True, blank=True)
    total_horas = models.CharField(max_length=5, null=True, blank=True, verbose_name='Total de Horas Hechas')

    def save(self, *args, **kwargs):
        if not self.validate_token():
            raise ValueError("Token inválido")
        if not self.has_previous_entry():
            raise ValueError("No hay registro de entrada previo")
        self.hora_salida = round_to_nearest_minute(self.hora_salida)
        self.calculate_hours()
        self.update_actividad_estado()
        super().save(*args, **kwargs)

    def validate_token(self):
        return self.token == self.alumno.token

    def has_previous_entry(self):
        return RegistroEntrada.objects.filter(alumno=self.alumno, fecha=self.fecha).exists()

    def calculate_hours(self):
        entrada = RegistroEntrada.objects.filter(alumno=self.alumno, fecha=self.fecha, hora_entrada__lte=self.hora_salida).order_by('-hora_entrada').first()
        if entrada:
            hentrada_dt = datetime.combine(self.fecha, entrada.hora_entrada)
            hsalida_dt = datetime.combine(self.fecha, self.hora_salida)
            delta = hsalida_dt - hentrada_dt
            total_horas = delta.total_seconds() / 3600  # Convertir segundos a horas

            self.total_horas = self.format_hours_minutes(total_horas)
        else:
            self.total_horas = '00:00'

    def update_actividad_estado(self):
        if not self.descripcion_actividad:
            self.descripcion_actividad = 'No hay actividades programadas'

    def format_hours_minutes(self, decimal_hours):
        hours = int(decimal_hours)
        minutes = int((decimal_hours - hours) * 60)
        return f'{hours:02}:{minutes:02}'

    def toJSON(self):
        item = model_to_dict(self)
        item['alumno'] = self.alumno.toJSON()
        item['hora_salida'] = self.hora_salida.strftime('%H:%M')
        item['fecha'] = self.fecha.strftime('%Y-%m-%d')
        item['total_horas'] = self.total_horas or '00:00'
        item['descripcion_actividad'] = self.descripcion_actividad or 'No hay actividades programadas'
        return item

    class Meta:
        verbose_name = 'Salida'
        verbose_name_plural = 'Salidas'

#########
class Actividad(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='actividades')
    nombre = models.CharField(max_length=200, verbose_name='Nombre de la Actividad')
    descripcion = models.TextField(verbose_name='Descripción de la Actividad', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')
    email_status = models.CharField(max_length=10, choices=Estados_Email, verbose_name='Estado del Envío de Email')

    def __str__(self):
        return f'{self.nombre} - {self.get_email_status_display()}'

    def toJSON(self):
        item = model_to_dict(self)
        item['alumno'] = self.alumno.toJSON()
        item['created_at'] = self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        item['email_status'] = self.get_email_status_display()
        return item

    def send_email(self, user):
        subject = f'Actividad Asignada: {self.nombre}'
        message = render_to_string('actividad/emails/nueva_actividad.html', {
            'alumno': self.alumno,
            'actividad': self,
            'user': user,
            'current_year': datetime.now().year
        })
        recipient_list = [self.alumno.email]
        email = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
        email.content_subtype = 'html'
        try:
            email.send()
            self.email_status = 'exitoso'
        except Exception as e:
            self.email_status = 'fallido'
            print(f"Error enviando correo: {e}")
        self.save(update_fields=['email_status'])

    def save(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().save(*args, **kwargs)
        if user:
            self.send_email(user)  # Enviar correo tanto al crear como al actualizar

    class Meta:
        verbose_name = 'Actividad'
        verbose_name_plural = 'Actividades'

########
