from .models import *
from datetime import datetime
from django.core.exceptions import ValidationError
from django import forms

class AlumnoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre_completo'].widget.attrs['autofocus'] = True

    class Meta:
        model = Alumno
        fields = '__all__'
        widgets = {
            'nombre_completo': forms.TextInput(attrs={'placeholder': 'Ingrese el nombre del Alumno'}),
            'telefono_celular': forms.TextInput(attrs={'placeholder': 'Ingrese un teléfono celular'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Ingrese un email'}),
            'modalidad': forms.Select(attrs={
                'class': 'select2',
                'style': 'width: 100%'
            }),
            'periodo_inicio': forms.DateInput(format='%Y-%m-%d', attrs={
                'class': 'form-control datetimepicker-input',
                'id': 'periodo_inicio',
                'value': datetime.now().strftime('%Y-%m-%d'),
                'data-toggle': 'datetimepicker',
                'data-target': '#periodo_inicio',
            }),
            'periodo_termino': forms.DateInput(format='%Y-%m-%d', attrs={
                'class': 'form-control datetimepicker-input',
                'id': 'periodo_termino',
                'value': datetime.now().strftime('%Y-%m-%d'),
                'data-toggle': 'datetimepicker',
                'data-target': '#periodo_termino',
            }),
            'token': forms.TextInput(attrs={'placeholder': 'En caso de requerir un Token específico ingréselo'}),
            'duracion_periodo': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese la duración del periodo en horas'
            }),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance

######
class HorarioForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['alumno'].widget.attrs['autofocus'] = True

    class Meta:
        model = Horario
        fields = '__all__'
        widgets = {
            'alumno': forms.Select(attrs={'class': 'form-select select2'}),
            'dia': forms.Select(attrs={
                'class': 'select2',
                'style': 'width: 100%'
            }),
            'programado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'hentrada': forms.TimeInput(format='%H:%M', attrs={
                'class': 'form-control datetimepicker-input',
                'id': 'hentrada',
                'value': datetime.now().strftime('%H:%M'),
                'data-toggle': 'datetimepicker',
                'data-target': '#hentrada'
            }),
            'hsalida': forms.TimeInput(format='%H:%M', attrs={
                'class': 'form-control datetimepicker-input',
                'id': 'hsalida',
                'value': datetime.now().strftime('%H:%M'),
                'data-toggle': 'datetimepicker',
                'data-target': '#hsalida'
            }),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance
        
#######
class RegistroEntradaForm(forms.ModelForm):
    alumno = forms.ModelChoiceField(queryset=Alumno.objects.all(), widget=forms.Select(attrs={'class': 'form-control select2'}))

    class Meta:
        model = RegistroEntrada
        fields = ['alumno', 'hora_entrada', 'fecha', 'token']
        widgets = {
            'hora_entrada': forms.TimeInput(format='%H:%M', attrs={
                'class': 'form-control datetimepicker-input',
                'id': 'hora_entrada',
                'value': datetime.now().strftime('%H:%M'),
                'data-toggle': 'datetimepicker',
                'data-target': '#hora_entrada'
            }),
            'fecha': forms.DateInput(format='%Y-%m-%d', attrs={
                'class': 'form-control datetimepicker-input',
                'id': 'fecha',
                'value': datetime.now().strftime('%Y-%m-%d'),
                'data-toggle': 'datetimepicker',
                'data-target': '#fecha',
            }),
            'token': forms.TextInput(attrs={'placeholder': 'Ingrese el token'})
        }

    def __init__(self, *args, **kwargs):
        is_edit = kwargs.pop('is_edit', False)
        super().__init__(*args, **kwargs)
        if not is_edit:
            self.fields['hora_entrada'].disabled = True
            self.fields['fecha'].disabled = True

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance



#######
class RegistroSalidaForm(forms.ModelForm):
    alumno = forms.ModelChoiceField(queryset=Alumno.objects.all(), widget=forms.Select(attrs={'class': 'form-control select2'}))

    class Meta:
        model = RegistroSalida
        fields = ['alumno', 'hora_salida', 'fecha', 'token', 'descripcion_actividad']
        widgets = {
            'hora_salida': forms.TimeInput(format='%H:%M', attrs={
                'class': 'form-control datetimepicker-input',
                'id': 'hora_salida',
                'value': datetime.now().strftime('%H:%M'),
                'data-toggle': 'datetimepicker',
                'data-target': '#hora_salida'
            }),
            'fecha': forms.DateInput(format='%Y-%m-%d', attrs={
                'class': 'form-control datetimepicker-input',
                'id': 'fecha',
                'value': datetime.now().strftime('%Y-%m-%d'),
                'data-toggle': 'datetimepicker',
                'data-target': '#fecha',
            }),
            'token': forms.TextInput(attrs={'placeholder': 'Ingrese el token', 'class': 'form-control'}),
            'descripcion_actividad': forms.Textarea(attrs={'placeholder': 'Describa la actividad realizada', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        is_edit = kwargs.pop('is_edit', False)
        super().__init__(*args, **kwargs)
        if not is_edit:
            self.fields['hora_salida'].disabled = True
            self.fields['fecha'].disabled = True

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance

#######
class ActividadForm(forms.ModelForm):
    class Meta:
        model = Actividad
        fields = ['alumno', 'nombre', 'descripcion']
        widgets = {
            'alumno': forms.Select(attrs={'class': 'form-control select2'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True, user=None):
        instance = super().save(commit=False)
        if commit:
            instance.save(user=user)
        return instance


######
class AsignacionHorasForm(forms.Form):
    alumno = forms.ModelChoiceField(queryset=Alumno.objects.all(), widget=forms.Select(attrs={'class': 'form-control select2'}))
    fecha = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d', attrs={
        'class': 'form-control datetimepicker-input',
        'data-toggle': 'datetimepicker',
        'data-target': '#fecha'
    }))
    hora_entrada = forms.TimeField(widget=forms.TimeInput(format='%H:%M', attrs={
        'class': 'form-control datetimepicker-input',
        'data-toggle': 'datetimepicker',
        'data-target': '#hora_entrada'
    }))
    hora_salida = forms.TimeField(widget=forms.TimeInput(format='%H:%M', attrs={
        'class': 'form-control datetimepicker-input',
        'data-toggle': 'datetimepicker',
        'data-target': '#hora_salida'
    }))
    token = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el token'}))
    descripcion_actividad = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describa la actividad realizada'}), required=False)

    def save(self, commit=True):
        cleaned_data = self.cleaned_data
        alumno = cleaned_data['alumno']
        fecha = cleaned_data['fecha']
        hora_entrada = cleaned_data['hora_entrada']
        hora_salida = cleaned_data['hora_salida']
        token = cleaned_data['token']
        descripcion_actividad = cleaned_data['descripcion_actividad']

        registro_entrada = RegistroEntrada(
            alumno=alumno,
            fecha=fecha,
            hora_entrada=hora_entrada,
            token=token
        )
        registro_entrada.save()

        registro_salida = RegistroSalida(
            alumno=alumno,
            fecha=fecha,
            hora_salida=hora_salida,
            token=token,
            descripcion_actividad=descripcion_actividad
        )
        registro_salida.save()

        return registro_entrada, registro_salida
